# AList Crypt 加解密工具

一个功能强大的桌面工具，用于**加密**和**解密** AList Crypt 文件。本工具使用 `rclone` 作为后端核心，提供图形用户界面（GUI）和命令行（CLI）两种操作方式，完全兼容 AList 的各项加密设置。

*(截图已更新为新版GUI界面示意)*

## 主要特性

- **图形用户界面 (GUI)**: 提供直观、易于上手的图形化操作界面，无需记忆复杂命令。
- **命令行界面 (CLI)**: 保留了强大的命令行模式，方便高级用户和自动化脚本调用。
- **双向操作**: 同时支持**加密**（将普通文件转换为加密文件）和**解密**（将加密文件还原为普通文件）。
- **完全兼容**: 支持 AList Crypt 的所有加密选项，包括文件名加密、目录名加密、密码混淆等。
- **跨平台**: 依赖 Python 和 rclone，可在 Windows, macOS, Linux 等多个平台上运行。

## 依赖

- Python 3.7+
- rclone

## 安装

1. 安装 Python 依赖

```bash
pip install pyyaml
```

2. **安装 rclone**
   - 从官网 [rclone.org/downloads/](https://rclone.org/downloads/) 下载并安装。
   - **重要**: 确保 `rclone` 的路径已添加到系统环境变量 `PATH` 中。你可以在终端输入 `rclone --version` 来验证。
3. **获取工具脚本**
   - 将 `crypto_gui.py` (图形界面) 和 `crypto_tool.py` (命令行核心) 这两个文件下载到你电脑的同一个目录下。

## 使用方法

我们提供两种使用方式，请根据你的偏好选择。

### 方式一：使用图形界面 (推荐)

这是最简单、最直观的使用方式。

1. 打开终端 (或 Windows 的 `cmd`/`PowerShell`)。

2. 使用 `cd` 命令进入你存放脚本的目录。

3. 运行以下命令启动图形界面：

   Bash

   ```
   python crypto_gui.py
   ```

4. 在弹出的窗口中，根据提示填写各项参数（操作类型、输入/输出目录、密码等），然后点击“开始执行”即可。

### 方式二：使用命令行

适合高级用户或需要自动化的场景。

#### **1. 加密文件**

**基本格式:**

Bash

```
python crypto_tool.py encrypt --input <明文源目录> --output <加密目标目录> --password <你的密码> [其他选项]
```

**示例:**

Bash

```
python crypto_tool.py encrypt --input "/path/to/my_documents" --output "/path/to/encrypted_backup" --password "your_password" --salt "your_salt"
```

#### **2. 解密文件**

**基本格式:**

Bash

```
python crypto_tool.py decrypt --input <加密源目录> --output <明文目标目录> --password <你的密码> [其他选项]
```

**示例:**

Bash

```
python crypto_tool.py decrypt --input "/path/to/encrypted_backup" --output "/path/to/restored_files" --password "your_password" --salt "your_salt"
```

## 可用参数

| **参数 (Parameter)**      | **说明 (Description)**                                       |
| ------------------------- | ------------------------------------------------------------ |
| `action`                  | **(必须)** 要执行的操作：`encrypt` (加密) 或 `decrypt` (解密)。 |
| `--input`                 | **(必须)** 输入目录。加密时为明文目录，解密时为加密目录。    |
| `--output`                | **(必须)** 输出目录。加密时为加密目录，解密时为明文目录。    |
| `--password`              | **(必须)** AList Crypt 密码。                                |
| `--salt`                  | AList Crypt 盐值 (可选)。                                    |
| `--filename-encryption`   | 文件名加密方式 (可选, 默认: `off`)。可选值: `off`, `standard`, `obfuscate`。 |
| `--directory-encryption`  | 是否加密目录名 (可选, 标志位, 默认: `false`)。               |
| `--suffix`                | 加密文件后缀 (可选, 默认: `.bin`)。                          |
| `--filename-encoding`     | 文件名编码方式 (可选, 默认: `base64`)。可选值: `base64`, `base32`, `base32768`。 |
| `--no-plaintext-password` | 若提供，表示密码和盐值是混淆形式 (可选, 标志位, 默认使用明文)。 |
| `--config`                | (已弃用，功能由命令行参数代替) 配置文件路径。                |

## 许可证

WTFPL v2 License
