import os
import time
import threading
from pypylon import pylon

os.environ['PYLON_CAMEMU'] = '1'

camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

print("Using device:", camera.GetDeviceInfo().GetModelName())

camera.AcquisitionFrameRateEnable.Value = True
camera.AcquisitionFrameRate.Value = 200
camera.ExposureTime.Value = 1000
camera.MaxNumBuffer.Value = 5

camera.Open()

TEST_DURATION = 5  # seconds
trigger_event = threading.Event()  


def simulated_trigger():
    start_time = time.time()
    while time.time() - start_time < TEST_DURATION:
        time.sleep(0.1)  # Simulated trigger interval
        trigger_event.set()  # Simulate external hardware trigger


def test_grab_strategy(strategy, output_queue_size=None):
    """Test different grab strategies using an emulated trigger event."""
    
    print(f"\nTesting strategy: {strategy}")

    if output_queue_size is not None:
        camera.OutputQueueSize.Value = output_queue_size

    # Start timing
    start_time = time.time()
    frame_count = 0
    skipped_frames = 0

    camera.StartGrabbing(strategy)

    trigger_thread = threading.Thread(target=simulated_trigger, daemon=True)
    trigger_thread.start()

    while time.time() - start_time < TEST_DURATION:
        if trigger_event.is_set():
            trigger_event.clear()
            camera.ExecuteSoftwareTrigger()

            grabResult = camera.RetrieveResult(100, pylon.TimeoutHandling_Return)
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
test_grab_strategy(pylon.GrabStrategy_LatestImages, output_queue_size=100)  # Keeps latest N frames

camera.Close()
