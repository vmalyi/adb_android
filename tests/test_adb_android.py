import sys, os, inspect, re, tempfile, unittest
adb_android = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],'../adb_android')))
if adb_android not in sys.path:
    sys.path.insert(0, adb_android)
import adb_android as adb

DEST_FOLDER_TARGET = '/data/media/0/'
NON_EXISTING_DIR = '/non-existing-dir/'
dest_folder_host = ''

ADB_COMMAND_PREFIX = 'adb'
ADB_COMMAND_SHELL = 'shell'
ADB_COMMAND_PULL = 'pull'
ADB_COMMAND_PUSH = 'push'
ADB_COMMAND_RM = 'rm -r'
ADB_COMMAND_CHMOD = 'chmod -R 777'
ADB_COMMAND_UNINSTALL = 'uninstall'
ADB_COMMAND_INSTALL = 'install'
ADB_COMMAND_FORWARD = 'forward'

tmp_file = None
tmp_file_on_target = None

path_to_valid_apk = 'files/valid.apk'
valid_package_name = 'com.example.android.valid'
path_to_invalid_apk = 'files/invalid.apk'
invalid_package_name = 'com.non-existing-app'
exp_install_cmd_output = re.compile(('package:' + valid_package_name))

adb_push = None
adb_pull = None

positive_exp_result_wo_output = 0, ''

def setUpModule():
    generate_tmp_file()

def generate_tmp_file():
    """Generates temp file and pushes it to target"""
    global tmp_file
    if not tmp_file:
        tmp_file = tempfile.NamedTemporaryFile(delete=True)
        print('*** preparing temporary file with name ' + tmp_file.name)
    adb.push(tmp_file.name, DEST_FOLDER_TARGET)

    #gets full path on target for tmp_file
    global tmp_file_on_target
    tmp_file_on_target = (DEST_FOLDER_TARGET + os.path.basename(tmp_file.name))
    print('*** getting path to tmp_file ' + str(tmp_file.name))

    #gets path to dest_folder_host
    global tmp_file
    global dest_folder_host
    dest_folder_host = os.path.dirname(tmp_file.name)
    print('*** getting path to dest_folder_host ' + dest_folder_host)

def is_emulator():
    result = adb.getserialno()
    if re.search('emulator.*', result[1]):
        print('True')
        return True
    else:
        print('False')
        return False

class TestPushCommand(unittest.TestCase):
    def test_push_p(self):
        global tmp_file
        global positive_exp_result_wo_output
        result = adb.push(tmp_file.name, DEST_FOLDER_TARGET)
        self.assertEqual(result, positive_exp_result_wo_output)

    def test_push_n_invalid_source_folder(self):
        global tmp_file
        result = adb.push(NON_EXISTING_DIR, DEST_FOLDER_TARGET)
        self.assertNotEqual(str(result), 0)

class TestPullCommand(unittest.TestCase):
    def test_pull_p(self):
        global tmp_file_on_target
        global dest_folder_host
        global positive_exp_result_wo_output
        result = adb.pull(tmp_file_on_target, dest_folder_host)
        self.assertEqual(result, positive_exp_result_wo_output)

    def test_pull_n_invalid_dest_folder_host(self):
        global tmp_file_on_target
        result = adb.pull(tmp_file_on_target, NON_EXISTING_DIR)
        self.assertNotEqual(str(result), 0)

class TestDevicesCommand(unittest.TestCase):
    def test_devices_p(self):
        result = adb.devices()
        #don't check output code in result but presence of "device" string
        self.assertRegexpMatches(result[1], '\\tdevice')

    def test_devices_p_l_option(self):
        result = adb.devices('-l')
        self.assertRegexpMatches(result[1], 'model:')

class TestShellCommand(unittest.TestCase):
    def test_shell_p(self):
        result = adb.shell('ls')
        #search for folders which will be for sure on Adnroid OS
        self.assertRegexpMatches(result[1], '(\\r\\nroot|\\r\\nsys|\\r\\nsystem)')

    def test_shell_p_w_option(self):
        result = adb.shell('ls -l')
        #search for time attribute which is for sure present in "-l" option
        self.assertRegexpMatches(result[1], '[0-2][0-9]:[0-5][0-9]')

    def test_shell_n_misspelled(self):
        result = adb.shell('misspelled')
        self.assertRegexpMatches(result[1], 'not found')

class TestExecCommand(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        """Prepares full adb commands for tests"""
        #assembles "adb push" command
        global tmp_file
        global adb_push
        adb_push = [ ADB_COMMAND_PREFIX, ADB_COMMAND_PUSH, tmp_file.name, \
        DEST_FOLDER_TARGET ]

        #assembles "adb pull" command
        global tmp_file_on_target
        global dest_folder_host
        global adb_pull
        adb_pull = [ ADB_COMMAND_PREFIX, ADB_COMMAND_PULL, tmp_file_on_target, \
        dest_folder_host ]

    def test_exec_p_adb_push(self):
        global adb_push
        global positive_exp_result_wo_output
        result = adb.exec_command(adb_push)
        self.assertEqual(result, positive_exp_result_wo_output)

    def test_exec_p_adb_pull(self):
        global adb_pull
        global positive_exp_result_wo_output
        result = adb.exec_command(adb_pull)
        self.assertEqual(result, positive_exp_result_wo_output)

    def test_exec_p_uncomplete_argument(self):
        #4th argument is missing in adb_command
        global positive_exp_result_wo_output
        adb_command = [ADB_COMMAND_PREFIX, ADB_COMMAND_PULL, tmp_file_on_target]
        result = adb.exec_command(adb_command)
        self.assertEqual(result, positive_exp_result_wo_output)

    def test_exec_n_missing_argument(self):
        #no argument at all
        adb_command = None
        result = adb.exec_command(adb_command)
        self.assertNotEqual(str(result), 0)

class TestInstallCommand(unittest.TestCase):
    @classmethod
    def setUp(self):
        """Deletes *.apk if it already installed"""
        global valid_package_name
        result = adb.shell('pm list packages | grep ' +  valid_package_name)
        if re.search(exp_install_cmd_output, result[1]):
            print('*** uninstalling existing ' + valid_package_name)
            adb.uninstall(valid_package_name)
        else:
            print('*** no need to uninstall ' + valid_package_name + ' since\
            it is not yet installed')

    @unittest.skipIf(is_emulator(), 'skip if run on emulator')
    def test_install_p(self):
        global path_to_valid_apk
        result = adb.install(path_to_valid_apk)
        self.assertRegexpMatches(result[1], 'Success')

    @unittest.skipIf(is_emulator(), 'skip if run on emulator')
    def test_install_p_reinstall(self):
        global path_to_valid_apk
        self.test_install_p()
        result = adb.install(path_to_valid_apk, '-r')
        self.assertRegexpMatches(result[1], 'Success')

    @unittest.skipIf(is_emulator(), 'skip if run on emulator')
    def test_install_p_sdcard(self):
        global path_to_valid_apk
        result = adb.install(path_to_valid_apk, '-s')
        self.assertRegexpMatches(result[1], 'Success')

    @unittest.skipIf(is_emulator(), 'skip if run on emulator')
    def test_install_p_all_opts(self):
        global path_to_valid_apk
        result = adb.install(path_to_valid_apk, '-r', '-s', '-l', '-d', '-t')
        self.assertRegexpMatches(result[1], 'Success')

    @unittest.skipIf(is_emulator(), 'skip if run on emulator')
    def test_install_n_invalid_apk(self):
        global path_to_invalid_apk
        result = adb.install(path_to_invalid_apk)
        self.assertRegexpMatches(result[1], 'INSTALL_FAILED_INVALID_APK')

class TestUninstallCommand(unittest.TestCase):
    @classmethod
    def setUp(self):
        """ Installs apk before test execution """
        global valid_package_name
        global path_to_valid_apk
        result = adb.shell('pm list packages | grep ' +  valid_package_name)
        if not re.search(exp_install_cmd_output, result[1]):
            print('*** installing ' + valid_package_name)
            adb.install(path_to_valid_apk)
        else:
            print('*** no need to install ' + valid_package_name + ' since it is\
            already installed')

    @unittest.skipIf(is_emulator(), 'skip if run on emulator')
    def test_uninstall_p(self):
        global valid_package_name
        result = adb.uninstall(valid_package_name)
        self.assertRegexpMatches(result[1], 'Success')

    @unittest.skipIf(is_emulator(), 'skip if run on emulator')
    def test_uninstall_keep_data(self):
        global valid_package_name
        result = adb.uninstall(valid_package_name, '-k')
        self.assertRegexpMatches(result[1], 'Success')

    @unittest.skipIf(is_emulator(), 'skip if run on emulator')
    def test_uninstall_n_invalid_package_name(self):
        global invalid_package_name
        result = adb.uninstall(invalid_package_name)
        self.assertRegexpMatches(result[1], 'DELETE_FAILED_INTERNAL_ERROR')

class TestGetSerialNoCommand(unittest.TestCase):
    def test_getserialno_p(self):
        result = adb.getserialno()
        self.assertNotRegexpMatches(result[1], 'unknown')

if __name__ == '__main__':
    unittest.main()
