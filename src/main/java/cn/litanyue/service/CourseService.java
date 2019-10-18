package cn.litanyue.service;

import cn.litanyue.pojo.Course;

import java.util.List;

public interface CourseService {

    public List<Course> findAll();
    public List<Course> findByJiaoxueban(String institute);
    public List<Course> findByJiaoshixingming(String teachername);
    public List<Course> findByKechengdaima(String code);
    public List<Course> findByKechengmingcheng(String curriculum);
    public List<Course> ResultCourse(String code);
}

