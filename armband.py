# Copyright (c) 2015  Niklas Rosenstein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import myo as libmyo; libmyo.init()
import time
import sys


class Listener(libmyo.DeviceListener):
    """
    Listener implementation. Return False from any function to
    stop the Hub.
    """

    interval = 0.05  # Output only 0.05 seconds

    def __init__(self):
        super(Listener, self).__init__()
        self.pose = libmyo.Pose.rest
        self.emg_enabled = False
        self.locked = False
        self.rssi = None
        self.emg = None
        self.last_time = 0
        self.timestamp = 0
        self.ax = 0
        self.ay = 0
        self.az = 0
        self.gx = 0
        self.gy = 0
        self.gz = 0
        self.ow = 0
        self.ox = 0
        self.oy = 0
        self.oz = 0

    def output(self):
        print(str(self.timestamp) + "," +
              str(self.ax)+"," + str(self.ay)+"," + str(self.az) +","+
              str(self.gx)+"," + str(self.gy)+"," + str(self.gz) +","+
              str(self.ox)+"," + str(self.oy)+"," + str(self.oz)+"," + str(self.ow)
              )

    def on_connect(self, myo, timestamp, firmware_version):
        myo.vibrate('short')
        myo.vibrate('short')
        myo.request_rssi()
        myo.request_battery_level()

    def on_rssi(self, myo, timestamp, rssi):
        self.rssi = rssi
        self.output()

    def on_pose(self, myo, timestamp, pose):
        pass

    def on_orientation_data(self, myo, timestamp, orientation):
        self.ox = orientation[0]
        self.oy = orientation[1]
        self.oz = orientation[2]
        self.ow = orientation[3]

    def on_accelerometor_data(self, myo, timestamp, acceleration):
        self.ax = acceleration[0]
        self.ay = acceleration[1]
        self.az = acceleration[2]
        self.timestamp = timestamp
        self.output()

    def on_gyroscope_data(self, myo, timestamp, gyroscope):
        self.gx = gyroscope[0]
        self.gy = gyroscope[1]
        self.gz = gyroscope[2]

    def on_emg_data(self, myo, timestamp, emg):
        pass

    def on_unlock(self, myo, timestamp):
        pass

    def on_lock(self, myo, timestamp):
        pass

    def on_event(self, kind, event):
        """
        Called before any of the event callbacks.
        """

    def on_event_finished(self, kind, event):
        """
        Called after the respective event callbacks have been
        invoked. This method is *always* triggered, even if one of
        the callbacks requested the stop of the Hub.
        """

    def on_pair(self, myo, timestamp, firmware_version):
        """
        Called when a Myo armband is paired.
        """

    def on_unpair(self, myo, timestamp):
        """
        Called when a Myo armband is unpaired.
        """

    def on_disconnect(self, myo, timestamp):
        """
        Called when a Myo is disconnected.
        """

    def on_arm_sync(self, myo, timestamp, arm, x_direction, rotation,
                    warmup_state):
        """
        Called when a Myo armband and an arm is synced.
        """

    def on_arm_unsync(self, myo, timestamp):
        """
        Called when a Myo armband and an arm is unsynced.
        """

    def on_battery_level_received(self, myo, timestamp, level):
        """
        Called when the requested battery level received.
        """

    def on_warmup_completed(self, myo, timestamp, warmup_result):
        """
        Called when the warmup completed.
        """


def main():
    try:
        hub = libmyo.Hub()
    except MemoryError:
        print("Myo Hub could not be created. Make sure Myo Connect is running.")
        return

    hub.set_locking_policy(libmyo.LockingPolicy.none)
    hub.run(1000, Listener())

    # Listen to keyboard interrupts and stop the hub in that case.
    try:
        while hub.running:
            time.sleep(0.25)
    except KeyboardInterrupt:
        print("\nQuitting ...")
    finally:
        print("Shutting down hub...")
        hub.shutdown()


if __name__ == '__main__':
    main()
