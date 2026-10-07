from app.core import Settings


def test_ignora_variables_desconocidas_del_env(tmp_path):
    """Un .env antiguo con UPLOAD_DIR (ya eliminada) no debe impedir arrancar."""
    env_file = tmp_path / ".env"
    env_file.write_text("UPLOAD_DIR=uploads\nAPP_NAME=Mi app\n", encoding="utf-8")

    settings = Settings(_env_file=env_file)

    assert settings.app_name == "Mi app"
