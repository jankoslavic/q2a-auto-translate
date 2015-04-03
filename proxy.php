<?php
/* A proxy file for dumping php arrays to json/pyhton. The argument
   specifies which file to dump. */


$var = include $argv[1];
echo json_encode($var);

?>