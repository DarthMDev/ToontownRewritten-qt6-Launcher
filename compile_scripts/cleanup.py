# the point of this script is to cleanup any unecessary files that are created during the compilation process
# this script is called by the main script after the compilation process is complete
 

# for qt6 we only need qtcore, qtgui, qtwidgets, QtWebEngineWidgets, and QtWebEngineCore
import os
import shutil
import sys
foldersToRemove = [
    # qt6 folders we do not need
    # bluetooth
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtBluetooth.framework",
    # concurrent
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtConcurrent.framework",
    # designer
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtDesigner.framework",
    # help
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtHelp.framework",
    # labs
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtLabsAnimation.framework",  
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtLabsFolderListModel.framework",
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtLabsQmlModels.framework",  
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtLabsSettings.framework",
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtLabsSharedImage.framework",
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtLabsWavefrontMesh.framework",
    # multimedia
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtMultimedia.framework",
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtMultimediaQuick.framework",
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtMultimediaWidgets.framework",
    # nfc 
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/Qtnfc.framework",
    # pdf
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtPdf.framework",
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtPdfQuick.framework",
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtPdfWidgets.framework",
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtQmlWorkerScript.framework",
    # all the quick3d frameworks
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtQuick3D.framework",
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtQuick3DAssetImport.framework",
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtQuick3DAssetUtils.framework"
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtQuick3DEffects.framework",
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtQuick3DHelpers.framework",
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtQuick3DIblBaker.framework",
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtQuick3DParticles.framework",
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtQuick3DRuntimeRender.framework",
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtQuick3DSpatialAudio.framework",
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtQuick3DUtils.framework",
    # quickcontrols2
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtQuickControls2.framework",
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtQuickControls2Impl.framework",
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtQuickDialogs2.framework",
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtQuickDialogs2QuickImpl.framework",
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtQuickDialogs2Utils.framework",
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtQuickLayouts.framework",
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtQuickParticles.framework",
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtQuickShapes.framework",
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtQuickTemplates2.framework",
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtQuickTest.framework",
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtQuickTimeline.framework",

    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QuickWidgets.framework",
    # remoteobjects
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtRemoteObjects.framework",
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtRemoteObjectsQml.framework",
    # sensors
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtSensors.framework",
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtSensorsQuick.framework",
    # serial port
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtSerialPort.framework",
    # shader tools
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtShaderTools.framework",
    # spartial audio
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtSpatialAudio.framework",
    # sql
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtSql.framework",
    # svg
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtSvg.framework",

    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtSvgWidgets.framework",
    # test
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtTest.framework",
    # texttospeech
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/lib/QtTextToSpeech.framework",
    # sql drivers we do not need
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/plugins/sqldrivers",
    # multimedia plugins we do not need
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/plugins/multimedia",
    # we dont need qml
    f"./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python{sys.version_info.major}.{sys.version_info.minor}/PyQt6/Qt6/qml",
]
    
for folder in foldersToRemove:
    try:
        print(f"Removing {folder}")
        shutil.rmtree(folder)
    except NotADirectoryError:
        os.remove(folder)
    except FileNotFoundError:
        print(f"Failed to remove {folder}")
        pass
    