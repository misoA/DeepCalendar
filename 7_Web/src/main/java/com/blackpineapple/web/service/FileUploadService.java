package com.blackpineapple.web.service;

import java.io.File;
import java.io.IOException;

import org.springframework.web.multipart.MultipartFile;

import com.amazonaws.services.s3.model.ObjectMetadata;

public interface FileUploadService {

	String uploadFile(MultipartFile file, String bucket_name, ObjectMetadata metadata) throws IOException;

}
