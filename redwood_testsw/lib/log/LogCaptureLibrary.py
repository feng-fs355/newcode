class LogCaptureLibrary(object):
    """
    This library is an abstract interface which defines APIs for log capturing.

    This library will import the actual implementation for various access point, for example,
    Android, iOS, Cloud, AP... etc.
    """

    ### *abstract functions ###
    def start_log_capture(self, path = None, file_name = None):
        """Start logging. path and file_name are optional.
        It will return the log capture ID for later use to stop.

        Examples:
        | start_log_capture |
        | start_log_capture | /my/log/dir |
        | start_log_capture | /my/log/dir | mycapture.log
        """
        raise Exception(NotImplemented)

    def stop_log_capture(self, log_id):
        """Stop logging. To stop a certain log capture.

        Examples:
        | stop_log_capture | ${log_id} |
        """
        raise Exception(NotImplemented)