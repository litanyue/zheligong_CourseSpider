package cn.litanyue.service.impl;

import cn.litanyue.dao.CourseDao;
import cn.litanyue.pojo.Course;
import cn.litanyue.service.CourseService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;
import org.springframework.stereotype.Service;

import java.util.List;


@Service
public class CourseServiceImpl implements CourseService {
    @Autowired
    private CourseDao courseDao;


    public List<Course> findByJiaoxueban(String institute) {
        return courseDao.findByJiaoxueban(institute);
    }

    public List<Course> findByJiaoshixingming(String teachername) {
        return courseDao.findByJiaoshixingming(teachername);
    }

    public List<Course> findByKechengdaima(String code) {
        return courseDao.findByKechengdaima(code);
    }

    public List<Course> ResultCourse(String code){return courseDao.ResultCode(code);}

    public List<Course> findByKechengmingcheng(String curriculum){return courseDao.findByKechengmingcheng(curriculum);}
    public List<Course> findAll() {
        return courseDao.findAll();
    }
}
