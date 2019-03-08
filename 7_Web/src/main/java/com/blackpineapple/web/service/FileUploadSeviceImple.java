package com.blackpineapple.web.service;

import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.util.Calendar;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.PropertySource;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import com.amazonaws.AmazonServiceException;
import com.amazonaws.auth.AWSCredentials;
import com.amazonaws.auth.BasicAWSCredentials;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3Client;
import com.amazonaws.services.s3.model.CannedAccessControlList;
import com.amazonaws.services.s3.model.ObjectMetadata;
import com.amazonaws.services.s3.model.PutObjectRequest;
import com.amazonaws.services.s3.model.PutObjectResult;

@Service
@PropertySource("classpath:config/properties/web.ALL.properties")
public class FileUploadSeviceImple implements FileUploadService {

	private static final Logger	logger	= LoggerFactory.getLogger(FileUploadSeviceImple.class);

	@Value("${aws.s3.accessKey}")
	private String				ACCESS_KEY;

	@Value("${aws.s3.secretKey}")
	private String				SECRET_KEY;


	@Override
	public String uploadFile(MultipartFile file, String bucket_name, ObjectMetadata metadata) throws IOException {
		AWSCredentials awsCredentials = new BasicAWSCredentials(ACCESS_KEY, SECRET_KEY);
		AmazonS3Client amazonS3 = new AmazonS3Client(awsCredentials);
		String url = "";
		String saveFilename = "";
		logger.info("------ bucket_name : " + bucket_name);
		
		
		if (amazonS3 != null) {
			try {
//				String filename = file.getName();
//				int pos = filename.lastIndexOf(".");
//				String fileExt = filename.substring(pos);

				saveFilename = String.format("%1$tY%1$tm%1$td%1$tH%1$tM%1$tS", Calendar.getInstance());
				saveFilename += System.nanoTime();
				String fileName = file.getOriginalFilename();
				int i = fileName.lastIndexOf(".");
				
				saveFilename += fileName.substring(i);

				PutObjectRequest putObjectRequest = new PutObjectRequest(bucket_name, saveFilename, file.getInputStream(), metadata);
				putObjectRequest.setCannedAcl(CannedAccessControlList.PublicRead); // file
																					// permission
				PutObjectResult result = amazonS3.putObject(putObjectRequest); // upload
																				// file
				URL upURL = amazonS3.getUrl(bucket_name, result.getSSECustomerKeyMd5());

				// result url
				url = upURL.toString() + saveFilename;
			} catch (AmazonServiceException ase) {
				ase.printStackTrace();
			} finally {
				amazonS3 = null;
			}
		}
		logger.info("------ upload done : " + bucket_name);
		return saveFilename;
	}
}
