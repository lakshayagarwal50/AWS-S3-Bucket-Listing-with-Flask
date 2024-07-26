import boto3
from flask import Flask, jsonify, request


# Create a Flask app instance
app = Flask(__name__)


def list_s3_buckets(sort_order="asc"):
  """
  This function retrieves a list of S3 buckets from your AWS account 
  and sorts them based on the provided sort order.

  Args:
      sort_order (str, optional): The order in which to sort the bucket names. 
                                  Valid options are "asc" (ascending) or "desc" 
                                  (descending). Defaults to "asc".

  Returns:
      list: A list of bucket names sorted according to the sort order.
            If an error occurs, a dictionary with an "error" key containing 
            the error message is returned.
  """
  try:
    # Create a boto3 S3 client
    s3_client = boto3.client('s3')

    # Get the list of S3 buckets
    buckets = s3_client.list_buckets()['Buckets']

    # Sort the bucket names based on sort order
    if sort_order.lower() == "asc":
      buckets.sort(key=lambda bucket: bucket['Name'])
    elif sort_order.lower() == "desc":
      buckets.sort(key=lambda bucket: bucket['Name'], reverse=True)
    else:
      return {"error": "Invalid sort order. Valid options are 'asc' or 'desc'"}

    # Return the list of bucket names
    return [bucket['Name'] for bucket in buckets]
  except Exception as e:
    # Handle exceptions
    return {"error": str(e)}


@app.route('/s3/buckets', methods=['GET'])
def get_s3_buckets():
  """
  This route handler retrieves a list of S3 buckets and returns them as a JSON response.
  It also allows specifying the sort order in the query string parameter "sort".

  Returns:
      JSON: A JSON response containing the list of bucket names or an error message.
  """
  # Get the sort order parameter from the request query string
  sort_order = request.args.get("sort", default="asc")
  bucket_list = list_s3_buckets(sort_order)
  if 'error' in bucket_list:
    return jsonify(bucket_list), 500
  return jsonify(bucket_list), 200


if __name__ == '__main__':
  app.run(debug=True)
