import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('validator', ROOT / 'scripts/validate_package.py')
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)

class PackageValidation(unittest.TestCase):
    def setUp(self):
        work = ROOT / '.test-work'
        work.mkdir(exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(prefix='check-', dir=work)
        self.root = Path(self.tmp.name) / 'package'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('.git', '__pycache__', '.test-work'))
    def tearDown(self):
        self.tmp.cleanup()
    def test_valid_package(self):
        self.assertEqual(validator.validate(self.root), [])
    def test_missing_reference_rejected(self):
        (self.root / 'skills/pm-define/references/prd-template.md').unlink()
        self.assertTrue(any('missing link' in e for e in validator.validate(self.root)))
    def test_escaped_reference_rejected(self):
        with (self.root / 'README.md').open('a') as f:
            f.write('\n[escape](../outside.md)\n')
        self.assertTrue(any('outside package' in e for e in validator.validate(self.root)))
    def test_secret_file_rejected(self):
        (self.root / '.env').write_text('EXAMPLE=synthetic')
        self.assertTrue(any('forbidden file' in e for e in validator.validate(self.root)))
    def test_version_mismatch_rejected(self):
        p = self.root / '.claude-plugin/plugin.json'
        p.write_text(p.read_text().replace('0.1.0', '0.2.0'))
        self.assertTrue(any('manifest mismatch' in e for e in validator.validate(self.root)))
    def test_symlink_rejected(self):
        (self.root / 'outside-link').symlink_to(self.root.parent)
        self.assertTrue(any('symlink' in e for e in validator.validate(self.root)))

if __name__ == '__main__':
    unittest.main()
