RGBanalysis
===========

## Description

This repository contains code for analysing color data over time collected using an open-hardware perovskite film degradation chamber described here: https://github.com/PV-Lab/hte_degradation_chamber

The picture data collected using the degradation chamber is analyzed with and without color calibration that is a method for collecting repeatable and reproducible color data from pictures. The code extracts the raw and color calibrated mean colors of each perovskite sample versus time during the aging test, and produces analysis graphs.

These analysis codes are part of an open-hardware project for developing degradation chambers for perovskite materials. The project is described in detail in our article: [insert details]

## Input Data

See an example of input picture data in folder "Data/Example_aging_test/". Details of the sample compositions and positions, as well as picture crop settings will be feeded in by the user in Main.py.

Assumptions:
- The input data folder contains only pictures.
  - The pictures are named according to the time of taking the picture in the format "YYYYMMDDhhmmss.bmp" (where YYYY is year, MM is month, DD is the day of the month, hh is hour in 24-h format, mm is minutes, and ss is seconds).
  - The first picture of the aging test is of XRite ColorChecker passport (a reference color chart required in the color calibration step).
  - All the other pictures have the sample holder and a small reference color chart (another chart required for following the longitudinal stability of the illumination intensity) in the picture area.
  - Layout described in detail in "Notes on Color Calibration and Sample Alignment".

## Output Data

See an example of output analysis results in folder "Results/Example_aging_test/".
- Folders
  - _Raw_: Not color calibrated
  - _Calibrated_: Color calibrated
  - _RGB_: Data presented in RGB (red, green, blue) format
  - _LAB_: Data presented in LAB format
- Files
  - _Samples.csv_: Sample details. All the data on the samples is presented in the same order than in this file.
  - _Times.csv_: Time points of the photos in the data. All the longitudinal data is presented in the same order than in this file.
  - _Samples.pdf_: Mean color of each sample by aging test duration in the same position than in the pictures
  - _Small_CC.pdf_: Mean color of each color patch in the reference color chart by aging test duration in the same position than in the pictures
  - Abbreviations in other filenames:
    - "_r_", "_g_", "_b_" (in folder _RGB_): Red, green, or blue pixel data, respectively
    - "_l_", "_a_", "_b_" (in folder _LAB_): LAB L, a, or b pixel data, respectively
    - "_sample_": Average sample colors vs. time (rows are samples, columns are time points)
    - "_CC_": Average colors of the color chart patches vs. time (rows are patches, columns are time points)
    - "_percentiles_hi_" or "_percentiles_lo_": 5% upper and lower percentiles of the color calculated from all the pixels provided for that sample
- Optional: Videos on the raw and calibrated aging test pictures can be produced if run in Linux.

## Notes on Color Calibration and Sample Alignment

The code produces color calibrated and raw color data as a function of measurement time. The use of color calibration is essential for ensuring repeatable and reproducible results. Approach implemented is described in detail in the ESI of the following article: https://doi.org/10.1016/j.matt.2021.01.008 

The assumptions of the code on the alignment of the sample holder, samples, and reference color charts:
- There is a sample holder with 4 (horizontal rows in the picture area) x 7 (vertical columns in the picture area) samples in the picture area during the aging test.
  - See "Sample locations and indexing.jpg" for an example of the sample positioning on a sample holder (A1 to D7) seen by a user standing in front of the degradation chamber, and how they are translated to the row indices (i) in the analysis results.
  - In the pictures, the sample holder alignment is such that D1 is in the upper left corner.

![Sample locations and indexing when the user stands in front of the degradation chamber.](https://github.com/PV-Lab/RGBanalysis/blob/master/Sample_locations_and_indexing.jpg)
  
- Use the same alignment of the sample holder, Xrite color chart, and small color chart than in the example data: "Data/Example_aging_test/". This ensures the right order of the samples in the resulting data files, and the correct color calibration in the color calibrated data.

![Example alignment of the sample holder and small color chart](https://github.com/PV-Lab/RGBanalysis/blob/master/Data/Example_aging_test/BMP/20190723161422.bmp)

- The reference colors for Xrite are hard-coded into the program. They need to be modified if another chart is used.

![Example alignment of the sample holder and small color chart](https://github.com/PV-Lab/RGBanalysis/blob/master/Data/Example_aging_test/BMP/20190723160422.bmp)

## Installation

Install Python programming platform Anaconda.

`$ git clone https://github.com/PV-Lab/RGBanalysis.git`

`$ cd RGBanalysis`

`$ conda env create -f environment.yml`

Activate environment "rgbanalysis".

To activate the video feature (Linux only): install ffmpeg (https://github.com/FFmpeg/FFmpeg).

Run Main.py.

## Use

- Open Main.py and modify according to the instructions in the file. Run.
  - If necessary, use Test_crop_box.py for determining suitable crop boxes. Crop boxes are used for slicing the sample holder image files into 28 individual samples, and for slicing the small reference color chart and Xrite Colorchecker Passport chart into color patches.
  - Video feature has been tested only in Linux and should be commented out in Main.py if using in Windows.
- Evaluate the validity color data:
  - Watch the videos if produced by the code. Ensure that:
    - Samples degrade as you expect (average color data produced in these codes, not spatial).
    - Color calibration results look natural (a wrong alignment of the Xrite color chart would produce gravely distorted colors).
    - Crop boxes (shown in the color calibrated video) are not misaligned.
  - Check that the degradation test illumination conditions remain constant, i.e., the photographed colors of the small reference color chart remains constant during the whole aging test. Any changes indicate issues with illumination conditions that can distort the color calibration results and degradation patterns of the samples.
  - This code assumes that none of the colors of the samples or color patches are saturated to white (RGB value of 256/256/256) or black (RGB value of 0/0/0). The color calibration results are not accurate if saturation appears so change the camera settings if this happens. Xrite white or black color patches, or very dark samples are prone to saturation.
  - This code assumes that the sample pictures are not affected by excessive reflections. Reflections decrease the quality of the data and can be fixed by adjusting the aging testing setup. 

## Versions

- 1.0 / Sep, 2020: Frozen version, in branch V1.0_frozen_year_2020
- 1.1 / May, 2020: Latest version

## Authors
||                    |
| ------------- | ------------------------------ |
| **AUTHORS**      | Armi Tiihonen, Zhe Liu, Siyu I.P. Tian | 
| **VERSION**      | 1.1 / May, 2022 | 
| **EMAILS**      | armi.tiihonen@gmail.com, chris.liuzhe@gmail.com, isaactsy777@hotmail.com  | 
||                    |


## Attribution

Please, acknowledge use of this work with the appropiate citation to the repository and research article.

## Citation

    @Misc{rgbanalysis2020,
      author =   {The RGBanalysis authors},
      title =    {{RGBanalysis}: Camera degradation data analysis with color calibration},
      howpublished = {\url{https://github.com/PV-Lab/RGBanalysis}},
      year = {2020}
    }
    
    [Insert details of the open HW paper]
    
    Shijing Sun, Armi Tiihonen, Felipe Oviedo, Zhe Liu, Janak Thapa, Yicheng Zhao, Noor Titan P. Hartono, Anuj Goyal, Thomas Heumueller, Clio Batali, Alex Encinas, Jason J. Yoo, Ruipeng Li, Zekun Ren, I. Marius Peters, Christoph J. Brabec, Moungi G. Bawendi, Vladan Stevanovic, John Fisher, Tonio Buonassisi, "A data fusion approach to optimize compositional stability of halide perovskites", Matter, 2021, https://doi.org/10.1016/j.matt.2021.01.008.
