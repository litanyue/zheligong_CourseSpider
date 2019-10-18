package cn.litanyue.dao;

import cn.litanyue.pojo.Course;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface CourseDao {
    List<Course> findAll();
    List<Course> findByJiaoxueban(String institute);
    List<Course> findByJiaoshixingming(String teachername);
    List<Course> findByKechengdaima(String code);
    List<Course> findByKechengmingcheng(String curriculum);
    List<Course> ResultCode(String code);

}
