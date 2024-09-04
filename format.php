<?php

function processMarkdownFiles($directory) {
    $files = new RecursiveIteratorIterator(
        new RecursiveDirectoryIterator($directory, RecursiveDirectoryIterator::SKIP_DOTS),
        RecursiveIteratorIterator::SELF_FIRST
    );

    foreach ($files as $file) {
        if ($file->isFile() && $file->getExtension() === 'md') {
            $content = file_get_contents($file->getPathname());
            $content = preg_replace('/(?<!\n)\n(?!\n)/', "  \n", $content);
            file_put_contents($file->getPathname(), $content);
            echo "Processed: " . $file->getPathname() . PHP_EOL;
        }
    }
}

$currentDirectory = __DIR__;
processMarkdownFiles($currentDirectory);

echo "All Markdown files have been processed.";
