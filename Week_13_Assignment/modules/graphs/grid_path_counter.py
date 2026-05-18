def CountGridPaths(rows, cols, step_fn=None):
    dp = [[0 for _ in range(cols)] for _ in range(rows)]

    for r in range(rows):
        for c in range(cols):

            if r == 0 and c == 0:
                dp[r][c] = 1
            else:
                up = dp[r - 1][c] if r > 0 else 0
                left = dp[r][c - 1] if c > 0 else 0
                dp[r][c] = up + left

            if step_fn:
                step_fn(dp, r, c)

    return dp[rows - 1][cols - 1]