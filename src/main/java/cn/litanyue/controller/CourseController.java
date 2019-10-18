package cn.litanyue.controller;

import cn.litanyue.pojo.Course;
import cn.litanyue.service.CourseService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.Date;
import java.util.List;

@Controller
//@RequestMapping("/course")
public class CourseController {

    @Autowired
    private CourseService courseService;

    @ResponseBody
    @RequestMapping("/findAll")
    public Course findAll(Model model){

        List<Course> courseList = courseService.findAll();
        System.out.println(courseList.size());

        model.addAttribute("one", courseList);
//        for(Course course:courseList){
//            System.out.println(course.getKechengmingcheng());
//        }
        return courseList.get(0);
    }





    //click 查具体课程 具体
    @ResponseBody
    @RequestMapping("/recommend")
    public List<Course> Recommend(){
        List<Course> courseList = courseService.findByJiaoshixingming("李");
        Date date = new Date();
        System.out.println(""+date.getHours()+date.getMinutes()+date.getSeconds());
        return courseList;
    }


    //下拉框 查学院的课 缩减
    @ResponseBody
    @RequestMapping("/courses/institute")
    public List<Course> findByJiaoxueban(@RequestParam("institute") String institute, Model model){
        List<Course> courseList = courseService.findByJiaoxueban(institute);
        model.addAttribute("courseList", courseList);
        return courseList;
    }


    //手动输入 查某代码的课 缩减
    @ResponseBody
    @RequestMapping("/courses/code")
    public List<Course> findByKechengdaima(@RequestParam("code") String code, Model model){
        List<Course> courseList = courseService.findByKechengdaima(code);
        model.addAttribute("courseList", courseList);
        return courseList;
    }
    //手动输入 查某个名称的课 缩减 模糊查询
    @ResponseBody
    @RequestMapping("/courses/curriculum")
    public List<Course> findByKechengmingcheng(@RequestParam("curriculum") String curriculum, Model model){
        List<Course> courseList = courseService.findByKechengmingcheng(curriculum);
        model.addAttribute("courseList", courseList);
        return courseList;
    }




    //手动输入 查教师的课 具体
    @ResponseBody
    @RequestMapping("/courses/teacher")
    public List<Course> findByJiaoshixingming(@RequestParam("teachername") String teachername, Model model){
        List<Course> courseList = courseService.findByJiaoshixingming(teachername);
        model.addAttribute("courseList", courseList);
        return courseList;
    }



    //click 查具体课程 具体
    @ResponseBody
    @RequestMapping("/course")
    public List<Course> ResultCourse(@RequestParam("code") String code, Model model){
        //差错检查
        List<Course> courseList = courseService.ResultCourse(code);
        model.addAttribute("courseList", courseList);
        return courseList;
    }

    @ResponseBody
    @RequestMapping("/aboutauthor")
    public String Aboutme(Model model){
        String aboutme = "<br>litanyue</br><br>977681262@qq.com</br>";
        return aboutme;
    }

}
