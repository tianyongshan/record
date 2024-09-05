<?php

/**

 format md file

 */
function processMarkdownFiles($directory) {
    $files = new RecursiveIteratorIterator(
        new RecursiveDirectoryIterator($directory, RecursiveDirectoryIterator::SKIP_DOTS),
        RecursiveIteratorIterator::SELF_FIRST
    );

    foreach ($files as $file) {
        if ($file->isFile() && $file->getExtension() === 'md') {
            $content = file_get_contents($file->getPathname());
            //$content = preg_replace('/(?<!\n)\n(?!\n)/', "  \n", $content);
            // 定义中文标点和对应的英文标点
            $chinesePunctuation = array(
                    '，' => ',',
                    '。' => '.',
                    '！' => '!',
                    '？' => '?',
                    '；' => '.',
                    ';' => '.',
                    '：' => '.',
                    '"' => '"',

                    '‘' => "'",
                    '”' => '"',
                    '（' => '(',
                    '）' => ')',
                    '【' => '[',
                    '】' => ']',
                    '《' => '<',
                    '》' => '>',
                    '、' => ',',
                    '…' => '...',
                    '—' => '-',
                    '～' => '~'
                    );

                // 使用 strtr 函数替换标点
                $content = strtr($content, $chinesePunctuation);
                file_put_contents($file->getPathname(), $content);
                echo "Processed: " . $file->getPathname() . PHP_EOL;
        }
    }
}

$currentDirectory = __DIR__;
processMarkdownFiles($currentDirectory);

echo "All Markdown files have been processed.";



