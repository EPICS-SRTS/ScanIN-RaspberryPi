<?php
/**
 * Created by PhpStorm.
 * User: ka7640
 * Date: 3/5/19
 * Time: 6:02 PM
 */

namespace SRTS\ScanIN\Hardware;


class multiThreader
{
    function newThread($data)
    {
        shell_exec("php threadedFile.php " . $data . " &");
    }
}