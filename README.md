# vits2-GPU-web
   java课程设计
 
  
    https://www.纯度.site 
  
  本VITS2-GPU-Web项目使用Spring Boot搭建了一个高性能且可扩展的VITS2语音合成服务。该服务提供了两个核心接口：获取语音模型接口和语音合成接口，并与React前端界面进行对接。在架构上，使用Nginx作为反向代理，将5000端口（Python）和4999端口（Java）分别与Python Flask和Spring Boot进行独立管理，实现了高效的前后端协同工作。
