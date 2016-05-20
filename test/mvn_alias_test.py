import unittest
import shutil
import os
from test_common import javautils_script, get_config_file_list, \
        get_actual_config, get_expected_config, \
        preload_xmvn_config, DIRPATH

from xml_compare import compare_xml_files

unordered = ['artifactGlob', 'alias', 'compatVersions']

class TestMvnAlias(unittest.TestCase):

    maxDiff = 2048

    def setUp(self):
        self.olddir = os.getcwd()
        self.workdir = os.path.join(DIRPATH, 'workdir')
        os.mkdir(self.workdir)
        os.chdir(self.workdir)

    def tearDown(self):
        try:
            shutil.rmtree(self.workdir)
        except OSError:
            pass
        os.chdir(self.olddir)

    @javautils_script('mvn_alias', [])
    def test_run_no_args(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertEqual("Usage:", stderr[:6])

    @javautils_script('mvn_alias', ['-h'])
    def test_help(self, stdout, stderr, return_value):
        self.assertTrue(stdout)

    @javautils_script('mvn_alias',['aaa:bbb', 'xxx:yyy', ])
    def test_simple(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        filelist = get_config_file_list()
        self.assertEqual(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_alias', 'simple'),
                 unordered)
            self.assertFalse(report, '\n' + report)

    @javautils_script('mvn_alias',['aaa:bbb', 'xxx:yyy:1.2', ])
    def test_version(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        filelist = get_config_file_list()
        self.assertEqual(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_alias', 'version'),
                 unordered)
            self.assertFalse(report, '\n' + report)

    @javautils_script('mvn_alias',['aaa:bbb', 'xxx:yyy:zzz:', ])
    def test_extension(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        filelist = get_config_file_list()
        self.assertEqual(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_alias', 'extension'),
                 unordered)
            self.assertFalse(report, '\n' + report)

    @javautils_script('mvn_alias',['aaa:bbb', 'xxx:yyy:zzz:www:', ])
    def test_classifier(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        filelist = get_config_file_list()
        self.assertEqual(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_alias', 'classifier'),
                 unordered)
            self.assertFalse(report, '\n' + report)

    @javautils_script('mvn_alias',['aaa:bbb:3.1', 'xxx:yyy:zzz:3.0', ])
    def test_comb1(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        filelist = get_config_file_list()
        self.assertEqual(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_alias', 'comb1'),
                 unordered)
            self.assertFalse(report, '\n' + report)

    @javautils_script('mvn_alias',['aaa:bbb:ccc:ddd:2.1', 'xxx:yyy:', ])
    def test_comb2(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        filelist = get_config_file_list()
        self.assertEqual(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_alias', 'comb2'),
                 unordered)
            self.assertFalse(report, '\n' + report)

    @javautils_script('mvn_alias',['aaa:bbb:ccc:', 'xxx:yyy:zzz:www:2.1', ])
    def test_comb3(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        filelist = get_config_file_list()
        self.assertEqual(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_alias', 'comb3'),
                 unordered)
            self.assertFalse(report, '\n' + report)

    @javautils_script('mvn_alias',['aaa:bbb:ccc:4.1', 'xxx:yyy:zzz:', ])
    def test_comb4(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        filelist = get_config_file_list()
        self.assertEqual(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_alias', 'comb4'),
                 unordered)
            self.assertFalse(report, '\n' + report)

    @javautils_script('mvn_alias',['aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' +
        'aaaaaaaaaaaaaaaaaaaaa:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb:c' +
        'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' +
        'cccccccccc:ddddddddddddddddddddddddddddddddddddddddddddddddddddd' +
        'ddddddddd:1111111111111111111111111111111111111',
        'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx:yyyyyyy' +
        'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy:zzzzzzzzzzzzzzzzzzzzz' +
        'zzzzzzzzzzzzzzzzzzzzzzzzzzz:wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww' +
        'wwwwwwwwwwwwwwwww:33333333333333333333333333333333333333333333'])
    def test_longopt(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        filelist = get_config_file_list()
        self.assertEqual(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_alias', 'longopt'),
                 unordered)
            self.assertFalse(report, '\n' + report)

    @javautils_script('mvn_alias',['*:aaa', 'xxx:yyy', ])
    def test_wildcard1(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        filelist = get_config_file_list()
        self.assertEqual(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_alias', 'wildcard1'),
                 unordered)
            self.assertFalse(report, '\n' + report)

    @javautils_script('mvn_alias',[':aaa', 'xxx:yyy', ])
    def test_wildcard2(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        filelist = get_config_file_list()
        self.assertEqual(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_alias', 'wildcard2'),
                 unordered)
            self.assertFalse(report, '\n' + report)

    @javautils_script('mvn_alias',['aaa::ccc', 'xxx:yyy', ])
    def test_wildcard3(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        filelist = get_config_file_list()
        self.assertEqual(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_alias', 'wildcard3'),
                 unordered)
            self.assertFalse(report, '\n' + report)

    @javautils_script('mvn_alias',['aaa:bbb', ])
    def test_one_argument(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @javautils_script('mvn_alias',['aaa:bbb', 'xxx', ])
    def test_invalid1(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @javautils_script('mvn_alias',['aaa', 'xxx:yyy', ])
    def test_invalid2(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @javautils_script('mvn_alias',['aaa:bbb', 'xxx:', ])
    def test_wildcard4(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        filelist = get_config_file_list()
        self.assertEqual(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_alias', 'wildcard4'),
                 unordered)
            self.assertFalse(report, '\n' + report)

    @javautils_script('mvn_alias',['a:b:c:d:e:f', 'x:y', ])
    def test_invalid5(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @javautils_script('mvn_alias',['a:b', 'x:y:z:w:1:e', ])
    def test_invalid6(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @javautils_script('mvn_alias',['aaa:bbb', 'ccc:ddd', 'eee:fff', 'ggg:hhh', ])
    def test_multi(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        filelist = get_config_file_list()
        self.assertEqual(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_alias', 'multi'),
                 unordered)
            self.assertFalse(report, '\n' + report)

    @javautils_script('mvn_alias',['aaa:bbb', 'ccc:ddd', 'eee:fff', ])
    def test_odd(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        filelist = get_config_file_list()
        self.assertEqual(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_alias', 'odd'),
                 unordered)
            self.assertFalse(report, '\n' + report)

    @javautils_script('mvn_alias',[':', ':', ])
    def test_wildcard7(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @javautils_script('mvn_alias',['x:y', 'a:b:c:*:1', ])
    def test_wildcard8(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @javautils_script('mvn_alias',['x:y', 'a:b:c::1', ])
    def test_wildcard9(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        filelist = get_config_file_list()
        self.assertEqual(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_alias', 'wildcard9'),
                 unordered)
            self.assertFalse(report, '\n' + report)

    @javautils_script('mvn_alias',['*:{aaa,bbb}*', ':@1', ])
    def test_backref(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        filelist = get_config_file_list()
        self.assertEqual(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_alias', 'backref'),
                 unordered)
            self.assertFalse(report, '\n' + report)

    @javautils_script('mvn_alias',['aaa', ':@1', ])
    def test_backref1(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @javautils_script('mvn_alias',['{aa,bb}:{cc,dd}', '@1:@2', ])
    def test_backref2(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        filelist = get_config_file_list()
        self.assertEqual(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_alias', 'backref2'),
                 unordered)
            self.assertFalse(report, '\n' + report)

    @javautils_script('mvn_alias',[':{aaa,bbb}', '@1:@2', ])
    def test_backref3(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @javautils_script('mvn_alias',[':{aaa,bbb', '@1', ])
    def test_odd_braces1(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @javautils_script('mvn_alias',[':{aaa,bbb}}', '@1', ])
    def test_odd_braces2(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @javautils_script('mvn_alias',['{aaa:bbb}:ccc', '@1', ])
    def test_braces(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    # for rhbz#1014301
    @javautils_script('mvn_alias',[':{woodstox-core}-asl', '@1-lgpl' ])
    def test_rhbz1014301(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertEqual(stderr.count("Artifact string '@1-lgpl' does not "
            "contain ':' character. Can not parse"),
                1)

    @preload_xmvn_config('mvn_alias', 'preexisting.xml')
    @javautils_script('mvn_alias',['aaa:bbb', 'xxx:yyy', ])
    def test_preexisting_unindexed(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        filelist = get_config_file_list()
        self.assertEqual(len(filelist), 2)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_alias', 'simple'),
                 unordered)
            self.assertFalse(report, '\n' + report)

    @preload_xmvn_config('mvn_alias', 'preexisting.xml',
            dstname='javapackages-config-00001.xml',
        update_index=True)
    @javautils_script('mvn_alias',['aaa:bbb', 'xxx:yyy', ])
    def test_preexisting(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        filelist = get_config_file_list()
        self.assertEqual(len(filelist), 2)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_alias', 'preexisting'),
                 unordered)
            self.assertFalse(report, '\n' + report)

if __name__ == '__main__':
    unittest.main()
