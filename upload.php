<?php

include "database.class.php";

use SRTS\ScanIN\Hardware\database as Database;

$database = new Database();



$database->connect();

$database->upload($argv[1]);