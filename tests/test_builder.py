def testBuildContext(self):
        #if IGNORE_TEST:
        #    return
        if os.path.isfile(CONTEXT_FILE):
            os.remove(CONTEXT_FILE)
        _ = ProjectBuilder.buildContext(context_file_path=CONTEXT_FILE, report_interval=1, first=0, last=2, data_dir=DATA_DIR)
        self.assertTrue(os.path.isfile(CONTEXT_FILE))
        with open(CONTEXT_FILE, "r") as fd:
            lines = fd.readlines()
        self.assertGreater(len(lines), 2)
        os.remove(CONTEXT_FILE)

def testBuildContext(self):
         if IGNORE_TEST:
             return
         if os.path.isfile(CONTEXT_FILE):
             os.remove(CONTEXT_FILE)
         _ = ProjectBuilder.buildContext(context_file_path=CONTEXT_FILE, report_interval=1, first=0, last=2, data_dir=DATA_DIR)                                                            
         self.assertTrue(os.path.isfile(CONTEXT_FILE))
         with open(CONTEXT_FILE, "r") as fd:
             lines = fd.readlines()
         self.assertGreater(len(lines), 2)
         os.remove(CONTEXT_FILE)
