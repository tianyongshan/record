<?php

// 获取当前目录下所有的 .md 文件
$files = glob("*.md");

foreach ($files as $file) {
    // 读取文件内容
    $content = file_get_contents($file);

    // 检查文件内容是否包含 '张千帆'
    if (strpos($content, '资中筠') === false) {
        // 如果不包含，删除文件
        if (unlink($file)) {
            echo "已删除文件: $file\n";
        } else {
            echo "无法删除文件: $file\n";
        }
    } else {
        echo "保留文件: $file\n";
    }
}

echo "处理完成\n";





