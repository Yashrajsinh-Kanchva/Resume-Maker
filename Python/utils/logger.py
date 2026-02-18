import logging
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Maximum lines before rotation
MAX_LINES = 500


class LineRotatingFileHandler(logging.FileHandler):
    """
    Custom file handler that rotates logs based on line count instead of file size.
    When log file exceeds MAX_LINES, it clears the file and starts fresh.
    """
    
    def __init__(self, filename, max_lines=MAX_LINES, mode='a', encoding=None, delay=False):
        self.max_lines = max_lines
        self.line_count = 0
        self._check_interval = 10  # Check file size every 10 writes for efficiency
        self._write_count = 0
        
        # Check current line count if file exists
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding=encoding or 'utf-8') as f:
                    self.line_count = sum(1 for _ in f)
            except Exception:
                self.line_count = 0
        
        super().__init__(filename, mode, encoding, delay)
    
    def emit(self, record):
        """
        Emit a record. Check line count periodically and rotate if needed.
        """
        # Check file line count periodically (every N writes) to avoid overhead
        self._write_count += 1
        if self._write_count >= self._check_interval:
            self._check_and_rotate()
            self._write_count = 0
        
        # Also check if we're close to limit before emitting
        if self.line_count >= self.max_lines:
            self._rotate_log()
        
        # Emit the record
        super().emit(record)
        self.line_count += 1
    
    def _check_and_rotate(self):
        """
        Check current line count in file and rotate if needed.
        This provides more accurate count by reading the actual file.
        """
        try:
            log_path = self.baseFilename
            if os.path.exists(log_path):
                # Re-count lines from actual file (more accurate)
                with open(log_path, 'r', encoding=self.encoding or 'utf-8') as f:
                    actual_count = sum(1 for _ in f)
                
                self.line_count = actual_count
                
                # Rotate if exceeded max lines
                if self.line_count >= self.max_lines:
                    self._rotate_log()
        except Exception:
            # If check fails, continue anyway
            pass
    
    def _rotate_log(self):
        """
        Rotate the log file by clearing it and resetting line count.
        Keeps last 100 lines as backup in .old file.
        """
        try:
            log_path = self.baseFilename
            backup_path = log_path + ".old"
            
            # Close current stream
            if self.stream:
                self.stream.close()
            
            # Read and backup last portion of log
            if os.path.exists(log_path):
                try:
                    with open(log_path, 'r', encoding=self.encoding or 'utf-8') as f:
                        lines = f.readlines()
                        # Keep last 100 lines as backup
                        backup_lines = lines[-100:] if len(lines) > 100 else lines
                    
                    # Write backup (overwrite old backup)
                    with open(backup_path, 'w', encoding=self.encoding or 'utf-8') as f:
                        f.writelines(backup_lines)
                except Exception:
                    pass
            
            # Clear the main log file
            with open(log_path, 'w', encoding=self.encoding or 'utf-8') as f:
                f.write("")  # Clear file
            
            # Reopen the file
            self.stream = self._open()
            self.line_count = 0
            self._write_count = 0  # Reset check counter
            
        except Exception as e:
            # If rotation fails, try to reopen anyway
            try:
                self.stream = self._open()
            except Exception:
                pass
            print(f"Log rotation error: {e}")


def setup_logger(name, log_file, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.handlers:
        return logger  # prevent duplicate handlers

    log_path = os.path.join(LOG_DIR, log_file)
    
    # Use custom LineRotatingFileHandler instead of RotatingFileHandler
    handler = LineRotatingFileHandler(
        log_path,
        max_lines=MAX_LINES,
        encoding='utf-8'
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def rotate_log_file(log_file, max_lines=MAX_LINES):
    """
    Manually rotate a specific log file if it exceeds max_lines.
    Useful for manual cleanup or startup checks.
    
    Args:
        log_file: Name of the log file (e.g., 'admin.log')
        max_lines: Maximum lines before rotation (default: MAX_LINES)
    
    Returns:
        bool: True if rotation occurred, False otherwise
    """
    log_path = os.path.join(LOG_DIR, log_file)
    
    if not os.path.exists(log_path):
        return False
    
    try:
        # Count lines
        with open(log_path, 'r', encoding='utf-8') as f:
            line_count = sum(1 for _ in f)
        
        if line_count >= max_lines:
            backup_path = log_path + ".old"
            
            # Read and backup last portion
            with open(log_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                backup_lines = lines[-100:] if len(lines) > 100 else lines
            
            # Write backup
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.writelines(backup_lines)
            
            # Clear main log
            with open(log_path, 'w', encoding='utf-8') as f:
                f.write("")
            
            return True
        
        return False
    except Exception as e:
        print(f"Error rotating log file {log_file}: {e}")
        return False


def rotate_all_logs(max_lines=MAX_LINES):
    """
    Check and rotate all log files in the logs directory that exceed max_lines.
    Useful for startup cleanup or scheduled maintenance.
    
    Args:
        max_lines: Maximum lines before rotation (default: MAX_LINES)
    
    Returns:
        dict: Dictionary with log file names as keys and rotation status as values
    """
    results = {}
    
    if not os.path.exists(LOG_DIR):
        return results
    
    try:
        for filename in os.listdir(LOG_DIR):
            if filename.endswith('.log') and not filename.endswith('.old'):
                results[filename] = rotate_log_file(filename, max_lines)
    except Exception as e:
        print(f"Error rotating logs: {e}")
    
    return results
