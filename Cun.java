package com.test;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;

import java.io.File;
import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Date;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Cun {
    private static final String DRIVER = "com.mysql.cj.jdbc.Driver";
    private static final String URL = "jdbc:mysql://localhost:3306/src?useUnicode=true&characterEncoding=utf8&serverTimezone=GMT%2B8&useSSL=false";
    private static final String NAME = "xxxxxxxxx";
    private static final String PASSWORD = "xxxxxxxx";


    public static void update(String sql) {
        Connection connection = null;
        Statement statement = null;
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            connection = DriverManager.getConnection(URL, NAME, PASSWORD);
            statement = connection.createStatement();

            int count = statement.executeUpdate(sql);
            if (count > 0) System.out.println("success");

        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        } catch (SQLException e) {
            e.printStackTrace();
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                if (statement != null) statement.close();
                if (connection != null) connection.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }

    }

    public static void main(String[] args) {
        Date date1 = new Date();
        System.out.println(date1);

        String kechengdaima = "";
        String kechengmingcheng = "";
        String xuefen = "";
        String kaibanshu = "";
        String jiaoshixingming = "";
        String jiaoxueban = "";
        String zhouxueshi = "";
        String kaohe = "";
        String shangkeshijian = "";
        String shangkedidian = "";
        String xiaoqv = "";
        String beizhu = "";
        String shoukefangshi = "";
        String shifouduanxueqi = "";
        String rongliang = "";
        String jiaocaimingcheng = "";


        String sql = "";

        //课程代码从这个字符串中取
        String path = "D:\\python_workspace\\schedule\\src1";
        File file = new File(path);        //获取其file对象
        File[] fs = file.listFiles();    //遍历path下的文件和目录，放在File数组中
        try {
            for (File f : fs) {
                path = f.getPath();         //得到文件路径
                Document doc = Jsoup.parse(new File(path), "GBK");
                Element tables = doc.getElementById("xjs_table");//找到包含课程信息的根结点，一门课程的所有信息
                Element tables_temp = tables.child(0);
                Integer count = tables_temp.childNodeSize() / 2;
                Element temp0 = doc.getElementById("Label1");
                String temptext = temp0.text();//要解析的字符串
                kechengmingcheng = temptext.substring(5, temptext.indexOf("学分："));
                kaibanshu = temptext.substring(temptext.lastIndexOf("：") + 1, temptext.length());
                String temp1 = null;
                Pattern r1 = Pattern.compile("\\d\\.\\d+");         //取学分值
                Matcher m1 = r1.matcher(temptext);
                m1.find();
                xuefen = m1.group();

                count = Integer.parseInt(kaibanshu);
                kechengdaima = path.substring(34, 39);      //操作感人
                for (int i = 1; i <= count; i++) {
                    Element temp = tables_temp.child(i);
                    jiaoshixingming = temp.child(1).child(0).text();
                    jiaoxueban = temp.child(2).text();
                    zhouxueshi = temp.child(3).text();
                    kaohe = temp.child(4).text();
                    shangkeshijian = temp.child(5).text();
                    shangkedidian = temp.child(6).text();
                    xiaoqv = temp.child(7).text();
                    beizhu = temp.child(8).text();
                    shoukefangshi = temp.child(9).text();
                    shifouduanxueqi = (temp.child(10).text() == null) ? "" : temp.child(10).text();
                    rongliang = temp.child(11).text();
                    jiaocaimingcheng = temp.child(12).child(0).text();
                    //拼接sql
                    sql = "insert into courses values(" +
                            "'" + kechengdaima + "'," +
                            "'" + kechengmingcheng + "'," +
                            "'" + xuefen + "'," +
                            "'" + kaibanshu + "'," +
                            "'" + jiaoshixingming + "'," +
                            "'" + jiaoxueban + "'," +
                            "'" + zhouxueshi + "'," +
                            "'" + kaohe + "'," +
                            "'" + shangkeshijian + "'," +
                            "'" + shangkedidian + "'," +
                            "'" + xiaoqv + "'," +
                            "'" + beizhu + "'," +
                            "'" + shoukefangshi + "'," +
                            "'" + shifouduanxueqi + "'," +
                            "'" + rongliang + "'," +
                            "'" + jiaocaimingcheng + "'" +
                            ")";
                    System.out.println(sql);

                    update(sql);

                }
                
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            Date date2 = new Date();
            System.out.println(date2);
        }

    }
}

