import os
import time
from pypylon import pylon

os.environ['PYLON_CAMEMU'] = '1'

camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

print("Using device:", camera.GetDeviceInfo().GetModelName())

camera.AcquisitionFrameRateEnable.Value = True
camera.AcquisitionFrameRate.Value = 200
camera.ExposureTimeAbs.Value = 500
camera.MaxNumBuffer.Value = 2

camera.Open()

TEST_DURATION = 5  # seconds


def test_grab_strategy(strategy, output_queue_size=None):
  
    print(f"\nTesting strategy: {strategy}")

    if output_queue_size is not None:
        camera.OutputQueueSize.Value = output_queue_size

    # Start timing
    start_time = time.time()
    frame_count = 0
    skipped_frames = 0

    camera.StartGrabbing(strategy)


    while time.time() - start_time < TEST_DURATION:
            camera.ExecuteSoftwareTrigger()

            grabResult = camera.RetrieveResult(100)
            if grabResult.IsValid():
                frame_count += 1
                skipped_frames += grabResult.GetNumberOfSkippedImages()

    camera.StopGrabbing()

    elapsed_time = time.time() - start_time
    fps = frame_count / elapsed_time
    print(f"Elapsed Time: {elapsed_time:.2f} seconds")
    print(f"Frames Retrieved: {frame_count}")
    print(f"FPS Achieved: {fps:.2f}")
    print(f"Skipped Frames: {skipped_frames}")


test_grab_strategy(pylon.GrabStrategy_OneByOne)  # Frame-by-frame processing
test_grab_strategy(pylon.GrabStrategy_LatestImageOnly)  # Keeps only the most recent frame
test_grab_strategy(pylon.GrabStrategy_LatestImages, output_queue_size=2)  # Keeps latest N frames

camera.Close()