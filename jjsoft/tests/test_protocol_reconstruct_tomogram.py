#!/usr/bin/env python

# ***************************************************************************
# *
# * Authors:     Daniel Del Hoyo (daniel.delhoyo.gomez@alumnos.upm.es)
# *
# * Unidad de Bioinformatica of Centro Nacional de Biotecnologia, CSIC
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************

from pyworkflow.tests import BaseTest, setupTestProject, DataSet
from pyworkflow.utils import greenStr

from jjsoft.protocols.protocol_reconstruct_tomogram import JjsoftReconstructTomogram

from tomo.protocols.protocol_ts_import import ProtImportTs


class TestTomogramReconstruction(BaseTest):

    @classmethod
    def setUpClass(cls):
        """Prepare the data that we will use later on."""
        setupTestProject(cls)  # defined in BaseTest, creates cls.proj
        cls.jjsoftDataTest = DataSet.getDataSet('tomo-em')
        cls.getFile = cls.jjsoftDataTest.getFile('etomo')


        def _runImportTiltSeries():
            protImport = cls.newProtocol(
                ProtImportTs,
                filesPath=cls.getFile,
                filesPattern='BB{TS}.st',
                minAngle=-55,
                maxAngle=65,
                stepAngle=2,
                voltage=300,
                magnification=105000,
                sphericalAberration=2.7,
                amplitudeContrast=0.1,
                samplingRate=1.35,
                doseInitial=0,
                dosePerFrame=0.3)
            cls.launchProtocol(protImport, wait=True)
            return protImport

        cls.setOfTs = _runImportTiltSeries().outputTiltSeries


    # The tests themselves.
    #
    def testReconstructionWBP(self):
        print ("\n", greenStr(" Test tomo3D reconstruction with WBP".center(75, '-')))

        # preparing and launching the protocol
        ptomo3D = self.proj.newProtocol(JjsoftReconstructTomogram,
                                        inputSetOfTiltSeries=self.setOfTs,
                                        method=0)
        self.proj.launchProtocol(ptomo3D, wait=True)
        setOfReconstructedTomograms = ptomo3D.outputTomograms

        # some general assertions
        self.assertIsNotNone(setOfReconstructedTomograms,
                             "There was some problem with the output")
        self.assertEqual(setOfReconstructedTomograms.getSize(), self.setOfTs.getSize(),
                         "The number of the denoised tomograms is wrong")

    def testReconstructionSIRT(self):
        print ("\n", greenStr(" Test tomo3D reconstruction with SIRT".center(75, '-')))

        # preparing and launching the protocol
        ptomo3D = self.proj.newProtocol(JjsoftReconstructTomogram,
                                        inputSetOfTiltSeries=self.setOfTs,
                                        method=1,
                                        nIterations=1)
        self.proj.launchProtocol(ptomo3D, wait=True)
        setOfReconstructedTomograms = ptomo3D.outputTomograms

        # some general assertions
        self.assertIsNotNone(setOfReconstructedTomograms,
                             "There was some problem with the output")
        self.assertEqual(setOfReconstructedTomograms.getSize(), self.setOfTs.getSize(),
                         "The number of the denoised tomograms is wrong")