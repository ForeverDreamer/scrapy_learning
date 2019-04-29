import scrapy
from scrapy.mail import MailSender


class StackoverflowEmailSpider(scrapy.Spider):

    name = 'email_notification'

    start_urls = ["https://stackoverflow.com/questions/"
                  "50249818/why-maven-assembly-works-when-sbt-assembly-find-conflicts"]

    def parse(self, response):

        answer_flag = response\
            .css("#answers-header > div > h2::text")\
            .re(r'(\d)\s[A-Z][a-z]+')
        
        if not answer_flag:
            
            self.logger.info("There are No Answers on this questions yet!")
        
        else:

            mailer = MailSender(
                                smtphost="smtp.gmail.com", 
                                mailfrom="scrapy.send@gmail.com", 
                                smtpuser="scrapy.send@gmail.com",
                                smtppass="Test_send_password.123",
                                smtpport=587
                                )
            
            msg_body = "Hi there,\n\nThere are " + answer_flag[0] + \
                       " answers to your question on stackoverflow. " + \
                       "Here's the link:\n" + response.url

            mailer.send(
                        to=["scrapy.receive@gmail.com"], 
                        subject="Someone responded to your question on your stackoverflow",
                        body=msg_body, cc=["scrapy.send@gmail.com"]
                        )
