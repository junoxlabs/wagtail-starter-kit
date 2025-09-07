from storages.backends.s3boto3 import S3Boto3Storage


class CustomS3Boto3Storage(S3Boto3Storage):
    """
    Custom S3 storage class that uses different endpoints for internal communication
    and external access (URL generation).
    """

    def __init__(self, *args, **kwargs):
        # Get the public endpoint URL from environment variable
        self.public_endpoint_url = kwargs.pop("public_endpoint_url", None)
        super().__init__(*args, **kwargs)

    def url(self, name):
        # If we have a public endpoint URL, use it for URL generation
        if self.public_endpoint_url and self.querystring_auth:
            # Save the original endpoint URL
            original_endpoint_url = self.endpoint_url
            # Temporarily set the public endpoint URL
            self.endpoint_url = self.public_endpoint_url
            # Generate the URL with query string authentication
            url = super().url(name)
            # Restore the original endpoint URL
            self.endpoint_url = original_endpoint_url
            return url
        else:
            return super().url(name)
