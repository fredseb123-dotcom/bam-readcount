#!/usr/bin/env python
"""This is a simple python script to perform an integration
test on bam-readcount. It uses a small BAM generated by merging
two 1000 Genomes sequencing for NA12878 and NA12892.
See https://github.com/genome/somatic-snv-test-data for info
on the BAMs and reference. These are subsets of the ones from that repo."""

import os
print "I AM IN", os.getcwd()
from integrationtest import IntegrationTest, main
from testdata import TEST_DATA_DIRECTORY
import unittest
import subprocess
import os

class TestBamReadcount(IntegrationTest, unittest.TestCase):

    def setUp(self):
        IntegrationTest.setUp(self)
        self.data_dir = TEST_DATA_DIRECTORY
        self.orig_path = os.path.realpath(os.getcwd())
        self.exe_path = os.path.realpath(self.exe_path)
        os.chdir(self.data_dir)

    def tearDown(self):
        IntegrationTest.tearDown(self)
        os.chdir(self.orig_path)

    def test_bamreadcount_normal(self):
        """test default output is as expected"""
        expected_file = "expected_all_lib"
        bam_file = "test.bam"
        ref_fasta = "ref.fa"
        site_list = "site_list"
        output_file = self.tempFile("output")
        cmdline = " ".join([self.exe_path, '-w', '1', '-f', ref_fasta, '-l', site_list, bam_file, '>', output_file])
        print "Executing", cmdline
        print "CWD", os.getcwd()
        rv = subprocess.call(cmdline, shell=True)
        print "Return value:", rv
        self.assertEqual(0, rv)
        self.assertFilesEqual(expected_file, output_file)
    def test_bamreadcount_perlib(self):
        """test per lib output is as expected"""
        expected_file = "expected_per_lib"
        bam_file = "test.bam"
        ref_fasta = "ref.fa"
        site_list = "site_list"
        output_file = self.tempFile("output")
        cmdline = " ".join([self.exe_path, '-w', '1', '-p', '-f', ref_fasta, '-l', site_list, bam_file, '>', output_file])
        print "Executing", cmdline
        print "CWD", os.getcwd()
        rv = subprocess.call(cmdline, shell=True)
        print "Return value:", rv
        self.assertEqual(0, rv)
        self.assertFilesEqual(expected_file, output_file) 

    def test_bamreadcount_normal_as_list(self):
        """test default output is as expected when list of regions passed at command-line"""
        expected_file = "expected_all_lib"
        bam_file = "test.bam"
        ref_fasta = "ref.fa"
        regions = "21:10402985-10402985 21:10405200-10405200"
        output_file = self.tempFile("output")
        cmdline = " ".join([self.exe_path, '-w', '1', '-f', ref_fasta, bam_file, regions, '>', output_file])
        print "Executing", cmdline
        print "CWD", os.getcwd()
        rv = subprocess.call(cmdline, shell=True)
        print "Return value:", rv
        self.assertEqual(0, rv)
        self.assertFilesEqual(expected_file, output_file)

    def test_bamreadcount_when_lib_absent(self):
        """test that we can run if there was no LB in the header"""
        expected_file = "expected_all_lib"
        bam_file = "test_bad_rg.bam"
        ref_fasta = "ref.fa"
        regions = "21:10402985-10402985 21:10405200-10405200"
        output_file = self.tempFile("output")
        cmdline = " ".join([self.exe_path, '-w', '1', '-f', ref_fasta, bam_file, regions, '>', output_file])
        print "Executing", cmdline
        print "CWD", os.getcwd()
        rv = subprocess.call(cmdline, shell=True)
        print "Return value:", rv
        self.assertEqual(0, rv)
        self.assertFilesEqual(expected_file, output_file)

    def test_bamreadcount_indel_centric_normal(self):
        """test all lib output, but with insertion centric counting"""
        expected_file = "expected_insertion_centric_all_lib"
        bam_file = "test.bam"
        ref_fasta = "ref.fa"
        site_list = "site_list"
        output_file = self.tempFile("output")
        cmdline = " ".join([self.exe_path, '-w', '1', '-i', '-f', ref_fasta, '-l', site_list, bam_file, '>', output_file])
        print "Executing", cmdline
        print "CWD", os.getcwd()
        rv = subprocess.call(cmdline, shell=True)
        print "Return value:", rv
        self.assertEqual(0, rv)
        self.assertFilesEqual(expected_file, output_file) 
        
    def test_bamreadcount_indel_centric_per_lib(self):
        """test all lib output, but with insertion centric counting"""
        expected_file = "expected_insertion_centric_per_lib"
        bam_file = "test.bam"
        ref_fasta = "ref.fa"
        site_list = "site_list"
        output_file = self.tempFile("output")
        cmdline = " ".join([self.exe_path, '-w', '1', '-i', '-p', '-f', ref_fasta, '-l', site_list, bam_file, '>', output_file])
        print "Executing", cmdline
        print "CWD", os.getcwd()
        rv = subprocess.call(cmdline, shell=True)
        print "Return value:", rv
        self.assertEqual(0, rv)
        self.assertFilesEqual(expected_file, output_file) 

if __name__ == "__main__":
    main()
