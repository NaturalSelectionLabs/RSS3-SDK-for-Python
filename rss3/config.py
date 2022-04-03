import os

max_value_length = 280
file_size_limit = int(os.getenv("FILE_SIZE_LIMIT") or 1024 * 1024)
version = "rss3.io/version/v0.3.1"
storage_expires = 14
