<?php

$directory = './';
$files = glob($directory . '*.md');

foreach ($files as $file) {
    $content = file_get_contents($file);

    // Add two spaces at the end of each line
    $content = preg_replace('/(?<!\s)$/m', '  ', $content);

    // Ensure paragraphs are separated by blank lines
    $content = preg_replace('/(\n)(?!\n)/', "\n\n", $content);

    file_put_contents($file, $content);
    echo "Processed: $file\n";
}

echo "All Markdown files have been updated.";
