import boto3
import os

from SendEmail import SendEmail

# Program to compare a target image with source images of source folder using compare_faces of AWS Rekognition
# Once match is found, get email Id and send mail through AWS SES

class CompareFaces:
    def __init__(self):
        print "Init ---"

    @staticmethod
    def compareFaces():

        output = None
        emailList = []
        session = boto3.Session(aws_access_key_id="",
                                aws_secret_access_key="")
        rek = session.client(service_name='rekognition', region_name='us-west-2')

        tarImgfile = open('img_path', 'rb')
        target = tarImgfile.read()
        tarImgfile.close()

        source = 'source_folder'
        for root, dirs, filenames in os.walk(source):
            print filenames
            for file in filenames:
                imgFile = r'source_folder'+'\\'+file                
                srcImgfile = open(imgFile, 'rb')
                source = srcImgfile.read()
                srcImgfile.close()

                rekresp = None
                rekresp = rek.compare_faces(SourceImage={'Bytes': source},TargetImage={'Bytes': target},
                                                   SimilarityThreshold = 95)

                if rekresp is not None:                    
                    if rekresp['FaceMatches'] is not None:
                        parameters = rekresp['FaceMatches']                    
                        if len(parameters) > 0:
                            print parameters[0].get('Similarity')
                            if(parameters[0].get('Similarity') >= 95):
                                email = file[0: len(file) - 4]                                
                                emailList.append(email)

        if emailList is not None and len(emailList) > 0:
            SendEmail.sendEmail(emailList, 'target_img_name')


CompareFaces.compareFaces();
