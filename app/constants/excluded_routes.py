# List of route prefixes to exclude from activity logging
# These routes will NOT create an entry in the activity_logs table

EXCLUDED_PREFIXES = {
    "/activity-logs": ["*"],    # exclude ALL methods for this route (to prevent recursion)
    "/loans": ["GET"],        # exclude GET
}
