/****************************************************************************
**
** Copyright (C) 2016 The Qt Company Ltd.
** Contact: https://www.qt.io/licensing/
**
** This file is part of the Qt Charts module of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:GPL$
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see https://www.qt.io/terms-conditions. For further
** information use the contact form at https://www.qt.io/contact-us.
**
** GNU General Public License Usage
** Alternatively, this file may be used under the terms of the GNU
** General Public License version 3 or (at your option) any later version
** approved by the KDE Free Qt Foundation. The licenses are as published by
** the Free Software Foundation and appearing in the file LICENSE.GPL3
** included in the packaging of this file. Please review the following
** information to ensure the GNU General Public License requirements will
** be met: https://www.gnu.org/licenses/gpl-3.0.html.
**
** $QT_END_LICENSE$
**
****************************************************************************/

import QtQuick 2.1
import QtQuick.Layouts 1.0

ColumnLayout {
    property alias openGLButton: openGLButton
    property alias antialiasButton: antialiasButton
    spacing: 8
    Layout.fillHeight: true
    signal animationsEnabled(bool enabled)
    signal seriesTypeChanged(string type)
    signal refreshRateChanged(variant rate)
    // signal signalSourceChanged(string source, int signalCount, int sampleCount); // REMOVED
    signal secondsChanged(variant seconds)
    signal antialiasingEnabled(bool enabled)
    signal openGlChanged(bool enabled)
    signal runChanged(bool enabled);  // ADDED

    Text {
        text: "Scope"
        font.pointSize: 18
        color: "white"
    }

    // ADDED
    MultiButton {
        id: runButton
        text: "Run: "
        items: ["false", "true"]
        currentSelection: 0
        onSelectionChanged: runChanged(currentSelection == 1);
    }

    MultiButton {
        id: openGLButton
        text: "OpenGL: "
        items: ["false", "true"]
        currentSelection: 1
        onSelectionChanged: openGlChanged(currentSelection == 1);
    }

    MultiButton {
        text: "Graph: "
        items: ["line", "scatter"]
        currentSelection: 0
        onSelectionChanged: seriesTypeChanged(items[currentSelection]);
    }

    // REMOVED signalSourceButton

    MultiButton {
        id: secondsButton
        text: "Seconds: "
        items: ["0.1", "0.5", "1", "5", "10"]
        currentSelection: 2
        onSelectionChanged: secondsChanged(items[currentSelection]);
    }

    MultiButton {
        text: "Refresh rate: "
        items: ["1", "24", "60"]
        currentSelection: 2
        onSelectionChanged: refreshRateChanged(items[currentSelection]);
    }

    MultiButton {
        id: antialiasButton
        text: "Antialias: "
        items: ["OFF", "ON"]
        enabled: true
        currentSelection: 0
        onSelectionChanged: antialiasingEnabled(currentSelection == 1);
    }
}
