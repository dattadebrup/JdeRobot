from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPixmap
from PyQt5.QtWidgets import QMainWindow, QAction, QDockWidget, QTreeView, QGraphicsView, \
    QWidget, QFileDialog, QLabel, QVBoxLayout, QPushButton, QMessageBox, QGraphicsItem, \
    QGraphicsScene

# from gui.automatascene import AutomataScene, OpType
# from gui.filemanager import FileManager
from gui.treemodel import TreeModel
from gui.state import State
from gui.transition import Transition
# from .state import State
# from .timerdialog import TimerDialog
# from .codedialog import CodeDialog
# from .librariesdialog import LibrariesDialog
# from .configdialog import ConfigDialog
# from gui.cppgenerator import CppGenerator
# from gui.pythongenerator import PythonGenerator
# import os


class RunTimeGui(QMainWindow):

    activeStateChanged = pyqtSignal(int)
    runningStateChanged = pyqtSignal(int)
    loadFromRoot = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__()

        self.setWindowTitle("VisualStates RunTime GUI")

        # # root state
        # self.rootState = State(0, "root", True)
        # self.activeState = self.rootState

        # create status bar
        self.statusBar()

        # self.createMenu()
        self.createTreeView()
        self.createStateCanvas()

        self.setGeometry(0, 0, 800, 600)
        self.show()

        self.states = {}
        self.transitions = {}

        self.activeState = None

        self.activeStateChanged.connect(self.activeStateChangedHandle)
        self.runningStateChanged.connect(self.runningStateChangedHandle)
        self.loadFromRoot.connect(self.loadFromRootHandle)

        # self.fileManager = FileManager()
        #
        # self.libraries = []
        # self.configs = []
        # self.interfaceHeaderMap = {}
        # self.createInterfaceHeaderMap()

    # def createMenu(self):
    #     # create actions
    #     # archieve menu
    #     newAction = QAction('&New', self)
    #     newAction.setShortcut('Ctrl+N')
    #     newAction.setStatusTip('Create New Visual States')
    #     newAction.triggered.connect(self.newAction)
    #
    #     openAction = QAction('&Open', self)
    #     openAction.setShortcut('Ctrl+O')
    #     openAction.setStatusTip('Open Visual States')
    #     openAction.triggered.connect(self.openAction)
    #
    #     saveAction = QAction('&Save', self)
    #     saveAction.setShortcut('Ctrl+S')
    #     saveAction.setStatusTip('Save Visual States')
    #     saveAction.triggered.connect(self.saveAction)
    #
    #     saveAsAction = QAction('&Save As', self)
    #     saveAsAction.setShortcut('Ctrl+S')
    #     saveAsAction.setStatusTip('Save Visual States as New One')
    #     saveAsAction.triggered.connect(self.saveAsAction)
    #
    #     quitAction = QAction('&Quit', self)
    #     quitAction.setShortcut('Ctrl+Q')
    #     quitAction.setStatusTip('Quit Visual States')
    #     quitAction.triggered.connect(self.quitAction)
    #
    #     # figures menu
    #     stateAction = QAction('&State', self)
    #     # stateAction.setShortcut('Ctrl+N')
    #     stateAction.setStatusTip('Create a state')
    #     stateAction.triggered.connect(self.stateAction)
    #
    #     transitionAction = QAction('&Transition', self)
    #     # transitionAction.setShortcut('Ctrl+T')
    #     transitionAction.setStatusTip('Create a transition')
    #     transitionAction.triggered.connect(self.transitionAction)
    #
    #     # data menu
    #     timerAction = QAction('&Timer', self)
    #     timerAction.setShortcut('Ctrl+M')
    #     timerAction.setStatusTip('Set timing of states')
    #     timerAction.triggered.connect(self.timerAction)
    #
    #     variablesAction = QAction('&Variables', self)
    #     variablesAction.setShortcut('Ctrl+V')
    #     variablesAction.setStatusTip('Define state variables')
    #     variablesAction.triggered.connect(self.variablesAction)
    #
    #     functionsAction = QAction('&Functions', self)
    #     functionsAction.setShortcut('Ctrl+F')
    #     functionsAction.setStatusTip('Define functions')
    #     functionsAction.triggered.connect(self.functionsAction)
    #
    #     # actions menu
    #     librariesAction = QAction('&Libraries', self)
    #     librariesAction.setShortcut('Ctrl+L')
    #     librariesAction.setStatusTip('Add additional libraries')
    #     librariesAction.triggered.connect(self.librariesAction)
    #
    #     configFileAction = QAction('&Config File', self)
    #     configFileAction.setShortcut('Ctrl+C')
    #     configFileAction.setStatusTip('Edit configuration file')
    #     configFileAction.triggered.connect(self.configFileAction)
    #
    #     generateCppAction = QAction('&Generate C++', self)
    #     generateCppAction.setShortcut('Ctrl+G')
    #     generateCppAction.setStatusTip('Generate C++ code')
    #     generateCppAction.triggered.connect(self.generateCppAction)
    #
    #     compileCppAction = QAction('&Compile C++', self)
    #     compileCppAction.setShortcut('Ctrl+P')
    #     compileCppAction.setStatusTip('Compile generated C++ code')
    #     compileCppAction.triggered.connect(self.compileCppAction)
    #
    #     generatePythonAction = QAction('&Generate Python', self)
    #     generatePythonAction.setShortcut('Ctrl+Y')
    #     generatePythonAction.setStatusTip('Generate Python code')
    #     generatePythonAction.triggered.connect(self.generatePythonAction)
    #
    #     # help menu
    #     aboutAction = QAction('&About', self)
    #     aboutAction.setShortcut('F1')
    #     aboutAction.setStatusTip('Information about VisualStates')
    #     aboutAction.triggered.connect(self.aboutAction)
    #
    #     # create main menu
    #     menubar = self.menuBar()
    #     archieveMenu = menubar.addMenu('&File')
    #     archieveMenu.addAction(newAction)
    #     archieveMenu.addAction(openAction)
    #     archieveMenu.addAction(saveAction)
    #     archieveMenu.addAction(saveAsAction)
    #     archieveMenu.addAction(quitAction)
    #
    #     figuresMenu = menubar.addMenu('&Figures')
    #     figuresMenu.addAction(stateAction)
    #     figuresMenu.addAction(transitionAction)
    #
    #     dataMenu = menubar.addMenu('&Data')
    #     dataMenu.addAction(timerAction)
    #     dataMenu.addAction(variablesAction)
    #     dataMenu.addAction(functionsAction)
    #
    #     actionsMenu = menubar.addMenu('&Actions')
    #     actionsMenu.addAction(librariesAction)
    #     actionsMenu.addAction(configFileAction)
    #     actionsMenu.addAction(generateCppAction)
    #     actionsMenu.addAction(compileCppAction)
    #     actionsMenu.addAction(generatePythonAction)
    #
    #     helpMenu = menubar.addMenu('&Help')
    #     helpMenu.addAction(aboutAction)

    # def createInterfaceHeaderMap(self):
    #     os.system('/opt/jderobot/bin/getinterfaces.sh /opt/jderobot/include/jderobot/slice > /tmp/allinterfaces.txt')
    #     fp = open('/tmp/allinterfaces.txt')
    #     for line in fp:
    #         data = line.split(' ')
    #         self.interfaceHeaderMap[data[0]] = data[1]


    # def newAction(self):
    #     self.clearScene()
    #     # create new root state
    #     self.rootState = State(0, 'root', True)
    #     self.automataScene.setActiveState(self.rootState)
    #     self.automataScene.resetIndexes()
    #
    # def openAction(self):
    #     fileDialog = QFileDialog(self)
    #     fileDialog.setWindowTitle("Open VisualStates File")
    #     fileDialog.setViewMode(QFileDialog.Detail)
    #     fileDialog.setNameFilters(['VisualStates File (*.xml)'])
    #     fileDialog.setDefaultSuffix('.xml')
    #     fileDialog.setAcceptMode(QFileDialog.AcceptOpen)
    #     if fileDialog.exec_():
    #         (self.rootState, self.configs, self.libraries) = self.fileManager.open(fileDialog.selectedFiles()[0])
    #         self.treeModel.removeAll()
    #         self.treeModel.loadFromRoot(self.rootState)
    #         # set the active state as the loaded state
    #         self.automataScene.setActiveState(self.rootState)
    #         self.automataScene.setLastIndexes(self.rootState)
    #     else:
    #         print('open is canceled')
    #
    #
    #
    # def saveAction(self):
    #     if len(self.fileManager.getFileName()) == 0:
    #         self.saveAsAction()
    #     else:
    #         self.fileManager.save(self.rootState, self.configs, self.libraries)
    #
    # def saveAsAction(self):
    #     fileDialog = QFileDialog(self)
    #     fileDialog.setWindowTitle("Save VisualStates Project")
    #     fileDialog.setViewMode(QFileDialog.Detail)
    #     fileDialog.setNameFilters(['VisualStates File (*.xml)'])
    #     fileDialog.setAcceptMode(QFileDialog.AcceptSave)
    #     if fileDialog.exec_():
    #         self.fileManager.setFullPath(fileDialog.selectedFiles()[0])
    #         self.fileManager.save(self.rootState, self.configs, self.libraries)
    #     else:
    #         print('file dialog canceled')
    #
    #
    # def quitAction(self):
    #     print('Quit')
    #     self.close()
    #
    # def stateAction(self):
    #     self.automataScene.setOperationType(OpType.ADDSTATE)
    #
    # def transitionAction(self):
    #     self.automataScene.setOperationType(OpType.ADDTRANSITION)
    #
    # def timerAction(self):
    #     if self.activeState is not None:
    #         timerDialog = TimerDialog('Time Step Duration', str(self.activeState.getTimeStep()))
    #         timerDialog.timeChanged.connect(self.timeStepDurationChanged)
    #         timerDialog.exec_()
    #
    # def variablesAction(self):
    #     if self.activeState is not None:
    #         variablesDialog = CodeDialog('Variables', self.activeState.getVariables())
    #         variablesDialog.codeChanged.connect(self.variablesChanged)
    #         variablesDialog.exec_()
    #     else:
    #         self.showWarning('Choose a state', 'You can create variables only for a selected state')
    #
    # def functionsAction(self):
    #     if self.activeState is not None:
    #         functionsDialog = CodeDialog('Functions', self.activeState.getFunctions())
    #         functionsDialog.codeChanged.connect(self.functionsChanged)
    #         functionsDialog.exec_()
    #     else:
    #         self.showWarning('Choose a state', 'You can create functions only for a selected state')
    #
    # def librariesAction(self):
    #     librariesDialog = LibrariesDialog('Libraries', self.libraries)
    #     librariesDialog.librariesChanged.connect(self.librariesChanged)
    #     librariesDialog.exec_()
    #
    # def configFileAction(self):
    #     configDialog = ConfigDialog('Config', self.configs)
    #     configDialog.configChanged.connect(self.configsChanged)
    #     configDialog.exec_()
    #
    #
    # def showWarning(self, title, msg):
    #     QMessageBox.warning(self, title, msg)
    #
    # def showInfo(self, title, msg):
    #     QMessageBox.information(self, title, msg)
    #
    # def generateCppAction(self):
    #     stateList = []
    #     if self.fileManager.hasFile():
    #         self.getStateList(self.rootState, stateList)
    #         generator = CppGenerator(self.libraries, self.configs, self.interfaceHeaderMap, stateList)
    #         generator.generate(self.fileManager.getPath(), self.fileManager.getFileName())
    #         self.showInfo('C++ Code Generation', 'C++ code generation is successful.')
    #     else:
    #         self.showWarning('C++ Generation', 'Please save the project before code generation.')
    #
    #
    # def compileCppAction(self):
    #     print('compile cpp action')
    #
    # def generatePythonAction(self):
    #     stateList = []
    #     if self.fileManager.hasFile():
    #         self.getStateList(self.rootState, stateList)
    #         generator = PythonGenerator(self.libraries, self.configs, self.interfaceHeaderMap, stateList)
    #         generator.generate(self.fileManager.getPath(), self.fileManager.getFileName())
    #         self.showInfo('Python Code Generation', 'Python code generation is successful.')
    #     else:
    #         self.showWarning('Python Generation', 'Please save the project before code generation.')

    # def aboutAction(self):
    #     print('about action')

    def createTreeView(self):
        dockWidget = QDockWidget()
        dockWidget.setAllowedAreas(Qt.LeftDockWidgetArea)
        dockWidget.setFeatures(QDockWidget.NoDockWidgetFeatures)
        dockWidget.setTitleBarWidget(QWidget())
        self.treeView = QTreeView()
        self.treeView.clicked.connect(self.treeItemClicked)
        self.treeModel = TreeModel()
        self.treeView.setModel(self.treeModel)

        self.logo = QLabel()
        logoPixmap = QPixmap('/usr/local/share/jderobot/resources/jderobot.png')
        self.logo.setPixmap(logoPixmap)

        self.upButton = QPushButton()
        self.upButton.setText('Up')
        self.upButton.clicked.connect(self.upButtonClicked)

        leftContainer = QWidget()
        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.treeView)
        leftLayout.addWidget(self.upButton)
        leftLayout.addWidget(self.logo)
        leftContainer.setLayout(leftLayout)

        dockWidget.setWidget(leftContainer)
        self.addDockWidget(Qt.LeftDockWidgetArea, dockWidget)

    def createStateCanvas(self):
        self.stateCanvas = QGraphicsView()
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 2000, 2000)
        # self.automataScene.activeStateChanged.connect(self.activeStateChanged)
        # self.automataScene.stateInserted.connect(self.stateInserted)
        # self.automataScene.stateRemoved.connect(self.stateRemoved)
        # self.automataScene.transitionInserted.connect(self.transitionInserted)
        # self.automataScene.stateNameChangedSignal.connect(self.stateNameChanged)

        self.setCentralWidget(self.stateCanvas)
        self.stateCanvas.setScene(self.scene)
        self.stateCanvas.setRenderHint(QPainter.Antialiasing)


    def addState(self, id, name, initial, x, y, parentId):
        if parentId is not None:
            self.states[id] = State(id, name, initial, self.states[parentId])
            self.states[parentId].addChild(self.states[id])
            parentItem = self.treeModel.getByDataId(parentId)
            print('parent:' + str(parentItem))
            # self.treeModel.insertState(self.states[id].getGraphicsItem(), Qt.white, parentItem)
        else:
            self.states[id] = State(id, name, initial, None)
            # self.treeModel.insertState(self.states[id].getGraphicsItem(), Qt.white)

        self.states[id].setPos(x, y)

    def addTransition(self, id, name, originId, destinationId, x, y):
        self.transitions[id] = Transition(id, name, self.states[originId], self.states[destinationId])
        self.transitions[id].setPos(x, y)

    def emitRunningStateById(self, id):
        self.runningStateChanged.emit(id)

    def runningStateChangedHandle(self, id):
        print('running state:' + str(id))
        runningState = self.states[id]
        if runningState.parent is not None:
            for child in runningState.parent.getChildren():
                child.getGraphicsItem().setRunning(False)
            runningState.getGraphicsItem().setRunning(True)
        self.treeModel.setAllBackground(Qt.white)
        self.treeModel.setBackgroundById(runningState.id, Qt.green)

    def emitActiveStateById(self, id):
        self.activeStateChanged.emit(id)

    def activeStateChangedHandle(self, id):
        self.activeState = self.states[id]
        print('set active state:' + str(id))
        self.scene.clear()
        for childState in self.activeState.getChildren():
            print('add child to scene:' + str(childState.id))
            qitem = childState.getGraphicsItem()
            qitem.setAcceptHoverEvents(False)
            qitem.setFlag(QGraphicsItem.ItemIsMovable, False)
            self.setAcceptDrops(False)
            self.scene.addItem(qitem)
            for tran in childState.getOriginTransitions():
                print('add transition:' + str(tran.id))
                qitem = tran.getGraphicsItem()
                qitem.disableInteraction()
                self.scene.addItem(qitem)

    def emitLoadFromRoot(self):
        self.loadFromRoot.emit(0)

    def loadFromRootHandle(self, id):
        self.treeModel.loadFromRoot(self.states[id])


    # def stateInserted(self, state):
    #     if self.activeState != self.rootState:
    #         parent = self.treeModel.getByDataId(self.activeState.id)
    #         self.treeModel.insertState(state, QColor(Qt.white), parent)
    #     else:
    #         self.treeModel.insertState(state, QColor(Qt.white))
    #
    # def stateRemoved(self, state):
    #     if self.activeState != self.rootState:
    #         self.treeModel.removeState(state.stateData, self.activeState)
    #     else:
    #         self.treeModel.removeState(state.stateData)
    #
    # def transitionInserted(self, tran):
    #     print('transition inserted:' + tran.transitionData.name)
    #
    # def stateNameChanged(self, state):
    #     dataItem = self.treeModel.getByDataId(state.stateData.id)
    #     if dataItem != None:
    #         dataItem.name = state.stateData.name
    #         self.treeModel.layoutChanged.emit()

    # def activeStateChanged(self):
    #     if self.automataScene.activeState != self.activeState:
    #         print('visual states active state changed:' + self.automataScene.activeState.name)
    #         self.activeState = self.automataScene.activeState
    #         if self.activeState == self.rootState:
    #             self.treeView.selectionModel().clearSelection()
    #         else:
    #             self.treeView.setCurrentIndex(self.treeModel.indexOf(self.treeModel.getByDataId(self.activeState.id)))

    def upButtonClicked(self):
        if self.activeState != None:
            if self.activeState.parent != None:
                print('parent name:' + self.activeState.parent.name)
                self.automataScene.setActiveState(self.activeState.parent)
                # if self.activeState.parent == self.rootState:
                #     self.treeView.selectionModel().clearSelection()
                #     print('clear selection')


    def getStateById(self,state, id):
        if state.id == id:
            return state
        else:
            result = None
            for child in state.getChildren():
                result = self.getStateById(child, id)
                if result is not None:
                    return result
            return result

    def treeItemClicked(self, index):
        print('clicked item.id:' + str(index.internalPointer().id))
        state = self.getStateById(self.rootState, index.internalPointer().id)
        if state is not None:
            # set the active state as the loaded state
            self.automataScene.setActiveState(state)

    # def timeStepDurationChanged(self, duration):
    #     if self.activeState is not None:
    #         self.activeState.setTimeStep(duration)
    #
    # def variablesChanged(self, variables):
    #     if self.activeState is not None:
    #         self.activeState.setVariables(variables)
    #
    # def functionsChanged(self, functions):
    #     if self.activeState is not None:
    #         self.activeState.setFunctions(functions)
    #
    # def librariesChanged(self, libraries):
    #     self.libraries = libraries
    #
    # def configsChanged(self, configs):
    #     self.configs = configs

    def getStateList(self, state, stateList):
        if len(state.getChildren()) > 0:
            stateList.append(state)

        for s in state.getChildren():
            self.getStateList(s, stateList)

