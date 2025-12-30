# These routes will NOT create an entry in the activity_logs table

EXCLUDED_PREFIXES = {
    "/activity-logs": ["*"],    # exclude all methods for this route 
    "/loans": ["GET"],        # exclude GET
}
