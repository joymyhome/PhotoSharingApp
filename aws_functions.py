"""
Call AWS services from here!
"""
import boto3
import utils
from image import Image
from botocore.exceptions import ClientError

BUCKET_NAME = 'photosharingapp-test'


def get_s3_image(image_id):
    """ Retrieve an object from AWS S3.

    :param image_id: string
    :return binary representation of an object. If it does not exist, return None
    """
    s3 = boto3.client('s3')
    try:
        return s3.get_object(Bucket=BUCKET_NAME, Key=image_id)['Body'].read()
    except ClientError as e:
        print(e)
        return None


def store_image_object(image_id, image_binary):
    """ Store image on AWS S3. image_id should be the same as for DynamoDB.

    :param image_id: string that uniquely identifies this image
    :param image_binary: binary file from user, jpg or jpeg
    :return None
    """
    image_name = image_id + ".jpg"
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_fileobj(image_binary, BUCKET_NAME, image_name)
    except ClientError as e:
        print(e)


def get_all_images(username):
    """
    Retrieve all image names from DynamoDB

    :param username: owner's name associated with images
    :return: array of strings, names of all images for this user
    """
    # TODO: retrieve information from DynamoDB and create array of objects of type Image
    # TODO: Remove everything below after implementing DynamoDB version
    # Retrieving all files from S3 and faking other data for Image object
    s3 = boto3.client('s3')
    resp = s3.list_objects_v2(Bucket=BUCKET_NAME)
    images_data = list()
    for obj in resp['Contents']:
        image_id = obj["Key"]
        description = "Description for image " + image_id + " and some smart text here! #AWS #working"
        images_data.append(Image(image_id=image_id, username=username, description=description, tags=list(), privacy=True))
    print(len(images_data))
    return images_data



def store_image_data(image_binary, username, description, privacy):
    """
    Store information on S3 and DynamoDB.
    DynamoDB table should consist at least on image_id, user_id, description, privacy (True or False), and tags.

    :param image_binary: binary file stored on S3 (I took care of this part)
    :param username: string, owner's name
    :param description: string, description of the image, can be an empty string
    :param privacy: boolean
    :return: None
    """
    image_id = utils.create_picID(username)
    # store image on AWS S3
    store_image_object(image_id, image_binary)
    # TODO: Write DynamoDB code storing all the image information (you don't need to use image_binary in DynamoDB, it is stored in S3)
    # split tags
    tags = utils.split_by_tag(description)
    # store image_id, description, tags, username, etc on DynamoDB
