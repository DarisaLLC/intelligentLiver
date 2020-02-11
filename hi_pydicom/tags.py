#------------------------------------------------------------------------------------------------------
#
#   Project - hI pydicom
#   Description:
#       An extension to pydicom
#   Author: huiliu.liu@gmail.com
#   Created 2020-01-04
#------------------------------------------------------------------------------------------------------

# general tags - patient
TagPatientName                                  = [0x0010, 0x0010]
TagPatientID                                    = [0x0010, 0x0020]
TagPatientAge                                   = [0x0010, 0x1010]
TagPatientSex                                   = [0x0010, 0x0040]
TagPatientWeight                                = [0x0010, 0x1030]

# general tags - timing
TagAcquisitionDate                              = [0x0008, 0x0022]
TagAcquisitionTime                              = [0x0008, 0x0032]

# general tags - study, series
TagStudyUID                                     = [0x0020, 0x000d]
TagStudyDate                                    = [0x0008, 0x0020]
TagStudyTime                                    = [0x0008, 0x0030]
TagSeriesUID                                    = [0x0020, 0x000e]
TagSeriesDate                                   = [0x0008, 0x0021]
TagSeriesTime                                   = [0x0008, 0x0031]
TagSeriesNumber                                 = [0x0020, 0x0011]
TagSeriesDescription                            = [0x0008, 0x103e]
TagSeriesNbSlices                               = [0x0054, 0x0081]


# general tags - machine
TagModality                                     = [0x0008, 0x0060]
TagManufacturer                                 = [0x0008, 0x0070]

# MR specific tags
TagMRAcquisitionType                            = [0x0018, 0x0023]
TagAcquisitionDuration                          = [0x0018, 0x9073]
TagSequenceName                                 = [0x0018, 0x0024]
TagTR                                           = [0x0018, 0x0080]
TagTE                                           = [0x0018, 0x0081]
TagFunc                                         = [0x0065, 0x102b]
TagEchoTime                                     = [0x0018, 0x0081]
TagEchoNumber                                   = [0x0018, 0x0086]
TagInstanceNumber                               = [0x0020, 0x0013]

# PET specific tags
TagActualFrameDuration                          = [0x0018, 0x1242]
TagSourceIsotopeName                            = [0x300a, 0x0226]
TagUnit                                         = [0x0054, 0x1001]

TagRadiopharmaceuticalInformationSequence       = [0x0054, 0x0016]
TagRadiopharmaceutical                          = [0x0018, 0x0031]
TagRadiopharmaceuticalStartDateTime             = [0x0018, 0x1078]
TagRadionuclideHalfLife                         = [0x0018, 0x1075]
TagRadionuclideTotalDose                        = [0x0018, 0x1074]

TagCorrectedImage                               = [0x0028, 0x0051]
TagDecayCorrection                              = [0x0054, 0x1102]

TagFrameReferenceTime                           = [0x0054, 0x1300]
TagDecayFactor                                  = [0x0054, 0x1321]
TagDoseCalibrationFactor                        = [0x0054, 0x1322]
TagScatterFractionFactor                        = [0x0054, 0x1323]

TagSeriesType                                   = [0x0054, 0x1000]
TagImageIndex                                   = [0x0054, 0x1330]
TagNbSlices                                     = [0x0054, 0x0081]
TagNbTimeSlices                                 = [0x0054, 0x0101]
