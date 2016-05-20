import os
import unittest

from javapackages.metadata.metadata import Metadata, MetadataInvalidException, MetadataLoadingException
from javapackages.metadata.artifact import MetadataArtifact
from javapackages.metadata.skippedartifact import MetadataSkippedArtifact
from javapackages.metadata.dependency import MetadataDependency

from test.misc import exception_expected


def depmapfile(fname):
    def test_decorator(fn):
        def test_decorated(self, *args, **kwargs):
            main_dir = os.path.dirname(os.path.realpath(__file__))
            fn(self, Metadata.create_from_file(os.path.join(main_dir, "data", fname)))
        return test_decorated
    return test_decorator


class TestDepmap(unittest.TestCase):

    @exception_expected(IOError)
    @depmapfile("NULL_FILE.xml")
    def test_nonexisting_depmap(self, d):
        self.assertTrue(False, "IOError was expected!")

    @depmapfile("depmap_compat_new.xml")
    def test_compat_new(self, d):
        pa = d.get_provided_artifacts()
        self.assertEqual(len(pa), 2)
        for a in pa:
            self.assertTrue(a.is_compat())

    @depmapfile("depmap_compat_new.xml")
    def test_java_requires(self, d):
        self.assertEqual(d.get_java_requires(), ["1.5"])

    @depmapfile("depmap_compat_new.xml")
    def test_java_devel_requires(self, d):
        self.assertEqual(d.get_java_devel_requires(), [])

    @depmapfile("depmap_compat_new.xml")
    def test_single_provides(self, d):
        self.assertEqual(len(d.get_provided_artifacts()), 2)

    @depmapfile("depmap_new_versioned.xml")
    def test_provided_mappings(self, d):
        artifacts = d.get_provided_artifacts()
        self.assertEqual(len(artifacts), 2)
        self.assertTrue(MetadataArtifact("org.apache.maven.plugins",
                                         "maven-idea-plugin",
                                         version="2.2",
                                         path="/usr/share/java/maven-idea-plugin/maven-idea-plugin.jar",
                                         properties={'requiresJava': '1.5'}
                                         ) in artifacts)
        self.assertTrue(MetadataArtifact("org.apache.maven.plugins",
                                         "maven-idea-plugin",
                                         version="2.2",
                                         extension="pom",
                                         path="/usr/share/maven-poms/JPP.maven-idea-plugin-maven-idea-plugin.pom")
                        in artifacts)

    @depmapfile("depmap_new_versioned_compressed.xml.gz")
    def test_compressed_depmap(self, d):
        artifacts = d.get_provided_artifacts()
        self.assertEqual(len(artifacts), 2)
        self.assertTrue(MetadataArtifact("org.apache.maven.plugins",
                                         "maven-idea-plugin",
                                         version="2.2",
                                         path="/usr/share/java/maven-idea-plugin/maven-idea-plugin.jar",
                                         properties={'requiresJava': '1.5'}
                                         ) in artifacts)
        self.assertTrue(MetadataArtifact("org.apache.maven.plugins",
                                         "maven-idea-plugin",
                                         version="2.2",
                                         path="/usr/share/maven-poms/JPP.maven-idea-plugin-maven-idea-plugin.pom",
                                         extension="pom") in artifacts)

    @depmapfile("depmap_new_compat.xml")
    def test_provided_versioned(self, d):
        artifacts = d.get_provided_artifacts()
        self.assertEqual(len(artifacts), 4)
        self.assertTrue(MetadataArtifact("org.apache.maven.plugins",
                                         "maven-idea-plugin",
                                         version="1.4",
                                         path="/usr/share/java/maven-idea-plugin/maven-idea-plugin-1.4.jar",
                                         compatVersions=set(['1.4'])) in artifacts)
        self.assertTrue(MetadataArtifact("org.apache.maven.plugins",
                                         "maven-idea-plugin",
                                         version="1.4",
                                         extension="pom",
                                         path="/usr/share/maven-poms/JPP.maven-idea-plugin-maven-idea-plugin-1.4.pom",
                                         compatVersions=set(["1.4"])) in artifacts)
        self.assertTrue(MetadataArtifact("org.apache.maven.plugins",
                                         "maven-idea-plugin",
                                         version="1.4",
                                         path="/usr/share/java/maven-idea-plugin/maven-idea-plugin-1.4.jar",
                                         compatVersions=set(["1.5"])) in artifacts)
        self.assertTrue(MetadataArtifact("org.apache.maven.plugins",
                                         "maven-idea-plugin",
                                         version="1.4",
                                         extension="pom",
                                         path="/usr/share/maven-poms/JPP.maven-idea-plugin-maven-idea-plugin-1.4.pom",
                                         compatVersions=set(["1.5"])) in artifacts)

    @exception_expected(MetadataInvalidException)
    @depmapfile("depmap_invalid_nover.xml")
    def test_no_maven_version(self, d):
        d.get_provided_artifacts()

    @exception_expected(MetadataInvalidException)
    @depmapfile("depmap_invalid_nover.xml")
    def test_no_maven_version_mappings(self, d):
        d.get_provided_artifacts()

    @depmapfile("depmap_compat_new.xml")
    def test_multiple_requires(self, d):
        reqs = d.get_required_artifacts()
        self.assertEqual(len(reqs), 8)

        self.assertTrue(MetadataDependency("org.apache.maven",
                                           "maven-project",
                                           requestedVersion="12") in reqs)

        self.assertTrue(MetadataDependency("org.codehaus.plexus",
                                           "plexus-container-default",
                                           requestedVersion="12") in reqs)

        self.assertTrue(MetadataDependency("org.codehaus.plexus",
                                           "plexus-utils",
                                           requestedVersion="12",
                                           extension="war") in reqs)

        self.assertTrue(MetadataDependency("org.apache.maven.wagon",
                                           "wagon-provider-api",
                                           requestedVersion="12",
                                           classifier="test-jar") in reqs)

    @depmapfile("depmap_namespace.xml")
    def test_namespace(self, d):
        artifacts = d.get_provided_artifacts()
        for a in artifacts:
            self.assertEqual(a.namespace, "ns")

    @depmapfile("depmap_multiple_namespaces.xml")
    def test_multiple_namespaces(self, d):
        prov = d.get_provided_artifacts()

        self.assertEqual(len(prov), 6)
        self.assertTrue(MetadataArtifact("org.codehaus.plexus",
                                         "plexus-utils",
                                         version="3.0",
                                         namespace="codehaus-plexus",
                                         path="/usr/share/java/plexus-utils/plexus-utils.jar",
                                         properties={'requiresJava': '1.5'}) in prov)

        self.assertTrue(MetadataArtifact("org.codehaus.plexus",
                                         "plexus-utils",
                                         version="3.0",
                                         extension="pom",
                                         namespace="codehaus-plexus",
                                         path="/usr/share/maven-poms/JPP.plexus-utils-plexus-utils.pom",
                                         properties={'requiresJava': '1.5'}) in prov)
        self.assertTrue(MetadataArtifact("plexus",
                                         "plexus-utils",
                                         version="1.2",
                                         namespace="plexus",
                                         path="/usr/share/java/plexus-utils/plexus-utils.jar",
                                         properties={'requiresJava': '1.5'}) in prov)
        self.assertTrue(MetadataArtifact("plexus",
                                         "plexus-utils",
                                         version="1.2",
                                         namespace="plexus",
                                         extension="pom",
                                         path="/usr/share/maven-poms/JPP.plexus-utils-plexus-utils.pom",
                                         properties={'requiresJava': '1.5'}) in prov)
        self.assertTrue(MetadataArtifact("codehaus",
                                         "plexus-utils",
                                         version="1.2",
                                         namespace="codehaus",
                                         path="/usr/share/java/plexus-utils/plexus-utils.jar",
                                         properties={'requiresJava': '1.5'}) in prov)
        self.assertTrue(MetadataArtifact("codehaus",
                                         "plexus-utils",
                                         version="1.2",
                                         namespace="codehaus",
                                         extension="pom",
                                         path="/usr/share/maven-poms/JPP.plexus-utils-plexus-utils.pom",
                                         properties={'requiresJava': '1.5'}) in prov)

    @depmapfile("depmap_namespace_requires.xml")
    def test_requires_namespace(self, d):
        reqs = d.get_required_artifacts()

        self.assertEqual(len(reqs), 12)

        self.assertTrue(MetadataDependency("org.apache.maven",
                                           "maven-project",
                                           requestedVersion="12") in reqs)

        self.assertTrue(MetadataDependency("org.codehaus.plexus",
                                           "plexus-utils",
                                           requestedVersion="12",
                                           namespace="plexus") in reqs)

        self.assertTrue(MetadataDependency("org.codehaus.plexus",
                                           "plexus-utils",
                                           requestedVersion="12",
                                           extension="war",
                                           namespace="codehaus") in reqs)

        self.assertTrue(MetadataDependency("org.codehaus.plexus",
                                           "plexus-utils",
                                           requestedVersion="12",
                                           resolvedVersion="0.9",
                                           namespace="test") in reqs)

        self.assertTrue(MetadataDependency("org.apache.maven.wagon",
                                           "wagon-provider-api",
                                           requestedVersion="12",
                                           classifier="test-jar") in reqs)

        self.assertTrue(MetadataDependency("org.codehaus.plexus",
                                           "plexus-container-default",
                                           requestedVersion="12") in reqs)

    @depmapfile("depmap_skipped.xml")
    def test_skipped(self, d):
        skipped = d.get_skipped_artifacts()

        self.assertEqual(len(skipped), 3)

        self.assertTrue(MetadataSkippedArtifact("org.apache.maven.plugins",
                                                "maven-idea-plugin") in skipped)

        self.assertTrue(MetadataSkippedArtifact("org.apache.maven.plugins",
                                                "maven-idea-plugin",
                                                extension="war") in skipped)

        self.assertTrue(MetadataSkippedArtifact("org.apache.maven.plugins",
                                                "maven-idea-plugin",
                                                classifier="test-jar") in skipped)

    @exception_expected(MetadataLoadingException)
    @depmapfile("depmap_incorrect_provides.xml")
    def test_incorrect_provides(self, d):
        pass

if __name__ == '__main__':
    unittest.main()
