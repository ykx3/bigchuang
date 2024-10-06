#include "libobsensor/ObSensor.hpp"
#include "opencv2/opencv.hpp"
#include <iostream>
#include <thread>
#include <chrono>
#include <stdexcept>

#define KEY_ESC 27

// Save the depth map in png format
void saveDepth(std::shared_ptr<ob::DepthFrame> depthFrame, int index) {
    std::vector<int> compression_params;
    compression_params.push_back(cv::IMWRITE_PNG_COMPRESSION);
    compression_params.push_back(0);
    compression_params.push_back(cv::IMWRITE_PNG_STRATEGY);
    compression_params.push_back(cv::IMWRITE_PNG_STRATEGY_DEFAULT);
    std::string depthName = "Depth_" + std::to_string(index) + ".png";
    cv::Mat depthMat(depthFrame->height(), depthFrame->width(), CV_16UC1, depthFrame->data());
    cv::imwrite(depthName, depthMat, compression_params);
    // std::cout << "Depth saved:" << depthName << std::endl;
}

// Save the color image in png format
void saveColor(std::shared_ptr<ob::ColorFrame> colorFrame, int index) {
    std::vector<int> compression_params;
    compression_params.push_back(cv::IMWRITE_PNG_COMPRESSION);
    compression_params.push_back(0);
    compression_params.push_back(cv::IMWRITE_PNG_STRATEGY);
    compression_params.push_back(cv::IMWRITE_PNG_STRATEGY_DEFAULT);
    std::string colorName = "Color_" + std::to_string(index) + ".png";
    cv::Mat colorRawMat(colorFrame->height(), colorFrame->width(), CV_8UC3, colorFrame->data());
    cv::imwrite(colorName, colorRawMat, compression_params);
    // std::cout << "Color saved:" << colorName << std::endl;
}

int main(int argc, char **argv) try {
    ob::Context::setLoggerSeverity(OB_LOG_SEVERITY_WARN);
    // create pipeline
    ob::Pipeline pipeline;
    int colorCount = 0;
    int depthCount = 0;
    // Configure which streams to enable or disable for the Pipeline by creating a Config
    std::shared_ptr<ob::Config> config = std::make_shared<ob::Config>();

    // Turn on D2C alignment, which needs to be turned on when generating RGBD point clouds
    std::shared_ptr<ob::VideoStreamProfile> colorProfile = nullptr;

    try {
        // Get all stream profiles of the color camera, including stream resolution, frame rate, and frame format
        auto colorProfiles = pipeline.getStreamProfileList(OB_SENSOR_COLOR);
        if(colorProfiles) {
            auto profile = colorProfiles->getProfile(OB_PROFILE_DEFAULT);
            colorProfile = profile->as<ob::VideoStreamProfile>();
        }
        config->enableStream(colorProfile);
    }
    catch(ob::Error &e) {
        config->setAlignMode(ALIGN_DISABLE);
        std::cerr << "Current device is not support color sensor!" << std::endl;
    }

    // Get all stream profiles of the depth camera, including stream resolution, frame rate, and frame format
    std::shared_ptr<ob::StreamProfileList> depthProfileList;
    OBAlignMode                            alignMode = ALIGN_DISABLE;
    if(colorProfile) {
        // Try find supported depth to color align hardware mode profile
        depthProfileList = pipeline.getD2CDepthProfileList(colorProfile, ALIGN_D2C_HW_MODE);
        if(depthProfileList->count() > 0) {
            alignMode = ALIGN_D2C_HW_MODE;
        }
        else {
            // Try find supported depth to color align software mode profile
            depthProfileList = pipeline.getD2CDepthProfileList(colorProfile, ALIGN_D2C_SW_MODE);
            if(depthProfileList->count() > 0) {
                alignMode = ALIGN_D2C_SW_MODE;
            }
        }
    }
    else {
        depthProfileList = pipeline.getStreamProfileList(OB_SENSOR_DEPTH);
    }

    if(depthProfileList->count() > 0) {
        std::shared_ptr<ob::StreamProfile> depthProfile;
        try {
            // Select the profile with the same frame rate as color.
            depthProfile = depthProfileList->getVideoStreamProfile(OB_WIDTH_ANY, OB_HEIGHT_ANY, OB_FORMAT_ANY, colorProfile->fps());
        }
        catch(...) {
            depthProfile = nullptr;
        }

        if(!depthProfile) {
            // If no matching profile is found, select the default profile.
            depthProfile = depthProfileList->getProfile(OB_PROFILE_DEFAULT);
        }
        config->enableStream(depthProfile);
    }
    config->setAlignMode(alignMode);
    // Create a format conversion Filter
    ob::FormatConvertFilter formatConvertFilter;
    // start pipeline with config
    pipeline.start(config);

    int frameCount = 0;
    while(true) {
        // Wait for up to 100ms for a frameset in blocking mode.
        auto frameset = pipeline.waitForFrames(100);
        if(frameset == nullptr) {
            std::cout << "The frameset is null!" << std::endl;
            continue;
        }

        // Filter the first 5 frames of data, and save it after the data is stable
        if(frameCount < 5) {
            frameCount++;
            continue;
        }

        // Get color and depth frames
        auto colorFrame = frameset->colorFrame();
        auto depthFrame = frameset->depthFrame();

        if(colorFrame != nullptr && colorCount < 1) {
            // save the colormap
            if(colorFrame->format() != OB_FORMAT_RGB) {
                if(colorFrame->format() == OB_FORMAT_MJPG) {
                    formatConvertFilter.setFormatConvertType(FORMAT_MJPG_TO_RGB888);
                }
                else if(colorFrame->format() == OB_FORMAT_UYVY) {
                    formatConvertFilter.setFormatConvertType(FORMAT_UYVY_TO_RGB888);
                }
                else if(colorFrame->format() == OB_FORMAT_YUYV) {
                    formatConvertFilter.setFormatConvertType(FORMAT_YUYV_TO_RGB888);
                }
                else {
                    std::cout << "Color format is not support!" << std::endl;
                    continue;
                }
                colorFrame = formatConvertFilter.process(colorFrame)->as<ob::ColorFrame>();
            }
            formatConvertFilter.setFormatConvertType(FORMAT_RGB888_TO_BGR);
            colorFrame = formatConvertFilter.process(colorFrame)->as<ob::ColorFrame>();
            saveColor(colorFrame, colorCount);
            colorCount++;
        }

        if(depthFrame != nullptr && depthCount < 1) {
            // save the depth map
            saveDepth(depthFrame, depthCount);
            depthCount++;
        }

        // Press the ESC key to exit the program when both the color image and the depth image are saved 5
        if(depthCount == 1 && (colorCount == 1 || colorCount == -1)) {
            break;
        }
    }
    pipeline.stop();
    return 0;
}
catch(ob::Error &e) {
    std::cerr << "function:" << e.getName() << "\nargs:" << e.getArgs() << "\nmessage:" << e.getMessage() << "\ntype:" << e.getExceptionType() << std::endl;
    return EXIT_FAILURE;
}
