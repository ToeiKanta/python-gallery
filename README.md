# Python Gallery

## Get Start
1. Go to program folder. </br>
`cd <program_path>`

2. install virtualenv </br>
`pip install virtualenv`

3. Create the virtual environment </br>
`virtualenv myenv`

4. activate virtualenv for Windowed  </br>
`Set-ExecutionPolicy Unrestricted -Scope Process` </br>
`.\myenv\Scripts\activate`

5. activate virtualenv for MacOS </br>
`source myenv/bin/activate`

6. install requirment </br>
`pip install -r requirements.txt`

## How to create exe file for Window OS

1. call pyinstaller command </br>
`pyinstaller -Fw --clean main.py`

2. copy Folder `./img` and `./icon.co` file to `./dist` folder

3. run program on `./dist/main.exe`

## Notes
- to save requirment </br>
`pip freeze > requirements.txt`

- Deactivate the virtual environment </br>
`deactivate`

## Search Image - Press Enter Key
![](readme/search.gif)

## Search Image - Realtime
![](readme/auto_search.gif)

## Page pagination
![](readme/pagination.gif)

## Edit image data - Embeded to image file
![](readme/edit_info.gif)


