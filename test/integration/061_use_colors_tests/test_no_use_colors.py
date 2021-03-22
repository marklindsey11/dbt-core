from test.integration.base import DBTIntegrationTest, use_profile
import re


class TestNoUseColors(DBTIntegrationTest):
    @property
    def project_config(self):
        return {"config-version": 2}

    @property
    def schema(self):
        return "use_colors_tests_061"

    @property
    def models(self):
        return "models"

    @use_profile("postgres")
    def test_postgres_no_use_colors(self):
        # pattern to match formatted log output
        pattern = re.compile(r"\[31m.*|\[33m.*")

        results, stdout = self.run_dbt_and_capture(
            args=["--no-use-colors", "run"], expect_pass=False
        )

        stdout_contains_formatting_characters = bool(pattern.search(stdout))
        self.assertFalse(stdout_contains_formatting_characters)
