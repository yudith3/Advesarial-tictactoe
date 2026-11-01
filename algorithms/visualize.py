import random
from .common import LINES, other, moves, winner, full, terminal_score


def heuristic(board, me):
    opp = other(me)
    weights = (0, 1, 5, 100)
    score = 0
    for line in LINES:
        cells = [board[r][c] for r, c in line]
        a, b = cells.count(me), cells.count(opp)
        if b == 0:
            score += weights[a]
        elif a == 0:
            score -= weights[b]
    return score


def build_tree(board, me, turn, algorithm="alphabeta", depth_limit=4, max_nodes=150):
    state = [row[:] for row in board]

    def board_state(b):
        return [row[:] for row in b]

    if algorithm == "mcts":
        rng = random.Random(2026)
        root = {
            "player": turn,
            "kind": "MCTS ROOT",
            "depth": 0,
            "move": None,
            "children": [],
            "label": "Root: kondisi papan saat ini",
            "state": board_state(state)
        }

        samples = 30

        for r, c in moves(state):
            child_board = [row[:] for row in state]
            child_board[r][c] = turn
            wins = draws = 0

            for _ in range(samples):
                sim = [row[:] for row in child_board]
                player = other(turn)

                while not winner(sim) and not full(sim):
                    rr, cc = rng.choice(moves(sim))
                    sim[rr][cc] = player
                    player = other(player)

                outcome = winner(sim)
                wins += outcome == turn
                draws += outcome is None

            rate = (wins + 0.5 * draws) / samples

            candidate_node = {
                "player": other(turn),
                "kind": "ROLLOUT",
                "depth": 1,
                "move": [r, c],
                "score": round(rate, 3),
                "visits": samples,
                "label": f"{samples} rollout · win-equivalent {rate:.1%}",
                "state": board_state(child_board),
                "children": []
            }

            rollout_board = board_state(child_board)
            rollout_player = other(turn)
            rollout_depth = 1
            path_cursor = candidate_node

            while not winner(rollout_board) and not full(rollout_board):
                rr, cc = rng.choice(moves(rollout_board))
                rollout_board[rr][cc] = rollout_player
                rollout_depth += 1

                path_node = {
                    "player": other(rollout_player),
                    "kind": "ROLLOUT",
                    "depth": rollout_depth,
                    "move": [rr, cc],
                    "score": None,
                    "label": f"Sampel langkah {rollout_player}",
                    "state": board_state(rollout_board),
                    "children": []
                }

                path_cursor["children"].append(path_node)
                path_cursor = path_node
                rollout_player = other(rollout_player)

            outcome = winner(rollout_board)
            path_cursor["terminal"] = True
            path_cursor["label"] = (
                "Hasil sampel: " + (outcome if outcome else "Seri")
            )

            root["children"].append(candidate_node)

        root["score"] = None

        def count_nodes(n):
            return 1 + sum(
                count_nodes(child)
                for child in n.get("children", [])
            )

        node_count = count_nodes(root)

        return {
            "tree": root,
            "nodes": node_count,
            "pruned": 0,
            "algorithm": algorithm,
            "note": (
                "Setiap kandidat menampilkan estimasi 30 rollout dan "
                "satu jalur rollout contoh dengan state di setiap langkah. "
                "Jalur contoh bersifat edukatif, bukan trace internal "
                "UCT produksi."
            )
        }

    counter = {
        "nodes": 0,
        "pruned": 0
    }

    def visit(b, player, depth, alpha, beta):
        counter["nodes"] += 1

        node = {
            "player": player,
            "kind": (
                "MAX" if player == me
                else (
                    "CHANCE"
                    if algorithm == "expectimax" and player != me
                    else "MIN"
                )
            ),
            "depth": depth,
            "move": None,
            "children": [],
            "pruned": False,
            "state": board_state(b)
        }

        terminal = terminal_score(b, me, depth)

        if terminal is not None:
            node.update(
                score=terminal,
                label=(
                    "Menang" if terminal > 0
                    else "Kalah" if terminal < 0
                    else "Seri"
                ),
                terminal=True
            )
            return terminal, node

        if algorithm == "dls" and depth >= max(1, int(depth_limit)):
            val = heuristic(b, me)
            node.update(
                score=val,
                label="Cutoff / heuristik",
                cutoff=True
            )
            return val, node

        legal = moves(b)

        if not legal:
            node.update(
                score=0,
                label="Seri",
                terminal=True
            )
            return 0, node

        vals = []

        for idx, (r, c) in enumerate(legal):
            remaining = len(legal) - idx

            if counter["nodes"] >= max_nodes - remaining:
                for rr, cc in legal[idx:]:
                    skipped_board = board_state(b)
                    skipped_board[rr][cc] = player

                    node["children"].append({
                        "move": [rr, cc],
                        "player": other(player),
                        "depth": depth + 1,
                        "state": skipped_board,
                        "pruned": True,
                        "label": "Tidak dieksplorasi (batas visualisasi)",
                        "children": []
                    })

                    counter["pruned"] += 1

                break

            b[r][c] = player

            val, child = visit(
                b,
                other(player),
                depth + 1,
                alpha,
                beta
            )

            b[r][c] = ""
            child["move"] = [r, c]
            node["children"].append(child)
            vals.append(val)

            if algorithm == "alphabeta":
                if player == me:
                    alpha = max(alpha, max(vals))
                else:
                    beta = min(beta, min(vals))

                if alpha >= beta:
                    skipped = len(legal) - idx - 1
                    counter["pruned"] += skipped

                    for rr, cc in legal[idx + 1:]:
                        skipped_board = board_state(b)
                        skipped_board[rr][cc] = player

                        node["children"].append({
                            "move": [rr, cc],
                            "player": other(player),
                            "depth": depth + 1,
                            "state": skipped_board,
                            "pruned": True,
                            "label": "Alpha-Beta cutoff",
                            "children": []
                        })

                    break

        if not vals:
            val = heuristic(b, me)
        elif algorithm == "expectimax" and player != me:
            val = sum(vals) / len(vals)
        else:
            val = max(vals) if player == me else min(vals)

        node["score"] = round(val, 2)
        node["label"] = (
            "Rata-rata peluang"
            if algorithm == "expectimax" and player != me
            else "Nilai minimax"
        )

        return val, node

    root_val, root = visit(
        state,
        turn,
        0,
        float("-inf"),
        float("inf")
    )

    return {
        "tree": root,
        "nodes": counter["nodes"],
        "pruned": counter["pruned"],
        "algorithm": algorithm,
        "note": (
            "Visualisasi dibatasi agar UI tetap responsif; "
            "node yang tidak ditampilkan diberi penanda."
        )
    }