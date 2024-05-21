import firebase_admin
from firebase_admin import credentials, firestore

# Intilialize Firebase
cred = credentials.Certificate("/home/alizeedrolet/sysc3010-project-l2-g6/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def add_data_to_firestore(collection_name: str, data: dict, doc_id: str):
    '''
    Function to add data to firestore
    
    Paramaters: 
        collection_name: Name of the firestore collection where the data is to be added
        data: Data to be added 
        Doc_ID: Unique ID of the document 
    

    '''
    try:
        doc_ref = db.collection(collection_name).document(doc_id)
        doc_ref.set(data)
    except Exception as error:
        print("Error adding data to firestore")
    
    
    
    
def get_user_from_firestore(username: str):
    '''
    Function to get user data based on usernmae.The username serves as the document id in the Users collection
    
    Paramaters:
        Username: username of the user
    
    Returns:
        Error if username is not found, returns user data if it is found
    '''
    
    try:
        user_reference = db.collection('Users').document(username)
        return user_reference.get().to_dict()
    except Exception as error:
        print("Error getting user")
        return None
            
        
def get_user_attribute(username: str,attribute: str) ->str:
    '''
    Function returns user attribute based on the username. The username serves as the document id in the Users collection
    Parameters:
        username: Username of the user
        attribute: Attribute to be returned. Options are name, username, email, phone number, password
    
    Returns: 
        Attribute value of the user sotred in the firetore. None if the user not found or a eception is raised 
    
    '''
        
    try:
        user_reference = db.collection('Users').document(username)
        user_data = user_reference.get()
        if user_data.exists:
            user_dict = user_data.to_dict()
            return user_dict.get(attribute)
        else:
            return None
    except Exception as error:
        print("Error getting user")
        return None




def get_user_names(username: str):
    try:
        # user_reference = db.collection('Users').document(username)
        # user_data = user_reference.get()
        # if user_data.exists:
        #     user_dict = user_data.to_dict()
        #     return user_dict.get(attribute)
        # else:
        #     return None
        return db.collection('Users').document(username).get().to_dict()
    except Exception as error:
        print("Error getting user")
        return None



def get_user_videos():
    """
    Retrieves URLs for videos stored in Firebase Cloud Storage.

    Returns:
        A list of public URLs to the videos.
    """
    try:
        print("before")
        # Specify your bucket name directly if it's not automatically resolved
        bucket_name = 'piguardian-bdb7e.appspot.com'  # Make sure to append .appspot.com to your bucket name
        bucket = storage.bucket(bucket_name)
        print("after bucket retrieval", bucket)

        blobs = bucket.list_blobs()  # List all blobs in the bucket

        video_urls = []
        for blob in blobs:
            # Optional: Check if the blob's content type is video
            if 'video' in blob.content_type:
                # Make the blob publicly accessible
                blob.make_public()

                # Append the public URL to the list of video URLs
                video_urls.append(blob.public_url)
        return video_urls
    except Exception as error:
        print(f"Error retrieving videos: {error}")
        return []

    

        
            
    




