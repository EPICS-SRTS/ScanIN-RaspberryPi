<?php
/**
 * Created by PhpStorm.
 * User: ka7640
 * Date: 3/5/19
 * Time: 5:49 PM
 */

namespace SRTS\ScanIN\Hardware;


use mysqli;

class database
{
    public $servername = "localhost";
    public $username = "srts";
    public $password = "123123";
    public $conn;

    function connect()
    {
        // Create connection
        $this->conn = new mysqli($this->servername, $this->username, $this->password);

        // Check connection
        if ($this->conn->connect_error) {
            die("Connection failed: " . $this->conn->connect_error);
        }
    }

    function upload($data)
    {
        $sql = "INSERT INTO `Data`(`Data`) VALUES ('" . $data . "')";
        $this->conn->query($sql);
    }

}

