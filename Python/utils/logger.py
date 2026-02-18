"""
Logging Utility Module

This module provides a custom logging handler that rotates log files based on
line count rather than file size. It includes utilities for setting up loggers
and managing log file rotation.

Features:
- Custom LineRotatingFileHandler for line-based rotation
- Automatic log rotation when files exceed MAX_LINES
- Backup of last 100 lines before rotation
- Manual rotation utilities for maintenance
"""

import logging
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Maximum lines before automatic rotation
MAX_LINES = 500


class LineRotatingFileHandler(logging.FileHandler):
    """
    Custom logging handler that rotates log files based on line count.
    
    When a log file exceeds the specified maximum lines, it automatically:
    1. Backs up the last 100 lines to a .old file
    2. Clears the main log file
    3. Continues logging from a fresh file
    
    This provides better control over log file sizes compared to size-based
    rotation, especially for applications with variable log line lengths.
    
    Attributes:
        max_lines: Maximum number of lines before rotation
        line_count: Current line count in the log file
        _check_interval: Number of writes before checking file size
        _write_count: Counter for writes since last check
    """
    
    def __init__(self, filename, max_lines=MAX_LINES, mode='a', encoding=None, delay=False):
        """
        Initialize the line-rotating file handler.
        
        Args:
            filename: Path to the log file
            max_lines: Maximum lines before rotation (default: MAX_LINES)
            mode: File open mode (default: 'a' for append)
            encoding: File encoding (default: None, uses system default)
            delay: Delay file opening until first emit (default: False)
        """
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
            # If rotation fails, try to reopen anyway to prevent logging failure
            try:
                self.stream = self._open()
            except Exception:
                pass
            # Use logging instead of print for error reporting
            logging.getLogger(__name__).error(f"Log rotation error for {log_path}: {e}", exc_info=True)


def setup_logger(name, log_file, level=logging.INFO):
    """
    Set up a logger with line-rotating file handler.
    
    Creates a logger instance with a custom handler that automatically rotates
    log files when they exceed MAX_LINES. Prevents duplicate handlers if
    called multiple times with the same name.
    
    Args:
        name: Logger name (typically module name)
        log_file: Name of the log file (e.g., 'admin.log')
        level: Logging level (default: logging.INFO)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent duplicate handlers if logger already exists
    if logger.handlers:
        return logger

    log_path = os.path.join(LOG_DIR, log_file)
    
    # Use custom LineRotatingFileHandler for line-based rotation
    handler = LineRotatingFileHandler(
        log_path,
        max_lines=MAX_LINES,
        encoding='utf-8'
    )

    # Configure log format: timestamp | level | logger_name | message
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
        logging.getLogger(__name__).error(f"Error rotating log file {log_file}: {e}", exc_info=True)
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
        logging.getLogger(__name__).error(f"Error rotating logs: {e}", exc_info=True)
    
    return results
