# NCRL_Huskey_CV

## Goal
* detect the green object (tennis).
* calculate the object's 3D coordinate with reference to camera.
* publish the object's position information to specific topic.

---

## Requirement
* Python3
* `pip install -r requirements.txt`

---

## Step
1. `$ roscore`
2. `$ python detect.py`
3. `$ rostopic echo /camera_coordinate`

---

## Result
* detect the green object.

![detect_pic](https://user-images.githubusercontent.com/40656204/74225602-ff2c1900-4cf5-11ea-8a7a-33ee69432255.png)

* calculate the object's 3D coordinate & publish the object's position to specific topic.

![position_pic](https://user-images.githubusercontent.com/40656204/74643233-57a85e00-51af-11ea-9a7f-9ad598a2cd1d.png)

---

## optimization
* noise reduction.

![](https://user-images.githubusercontent.com/40656204/74717389-458bf580-526b-11ea-8c64-d8a30c804546.png)