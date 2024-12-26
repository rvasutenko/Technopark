TEMPLATE = app
CONFIG += console c++17
CONFIG -= app_bundle
CONFIG -= qt

SOURCES += \
    arcgraph.cpp \
    listgraph.cpp \
        main.cpp \
 \        # my_stream.cpp
    matrixgraph.cpp \
    setgraph.cpp

HEADERS += \
    arcgraph.h \
    igraph.h \
    listgraph.h \
    main.h \
    matrixgraph.h \
    setgraph.h
    # main.h \
