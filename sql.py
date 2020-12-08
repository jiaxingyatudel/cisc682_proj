#create tables
sql_create_tables="""
drop database if exists cisc637;
create database cisc637;
use cisc637;

create table user_info(
    user_id varchar(255),
    user_name varchar(255),
    primary key (user_id)
);

create table user_security(
    user_id varchar(255),
    user_email varchar(255),
    user_password varchar(255),
    primary key (user_id),
    foreign key (user_id) references user_info(user_id) on delete cascade,
    unique (user_email)
);

create table user_cookie(
    user_id varchar(255),
    user_cookie_value varchar(255),
    user_cookie_time_stamp int,
    primary key (user_cookie_value),
    foreign key (user_id) references user_info(user_id) on delete cascade
);

create table user_follow(
    user_id varchar(255),
    follow_id varchar(255),
    foreign key (user_id) references user_info(user_id) on delete cascade,
    foreign key (follow_id) references user_info(user_id) on delete cascade
);

create table post_info(
    post_id varchar(255),
    post_title text,
    post_text text,
    post_time datetime,
    user_id varchar(255),
    primary key (post_id),
    foreign key (user_id) references user_info(user_id) on delete cascade
);

create table post_ingredient(
    post_id varchar(255),
    ingredient_id varchar(255),
    ingredient_text text,
    foreign key (post_id) references post_info(post_id) on delete cascade
);

create table user_like_post(
    user_id varchar(255),
    post_id varchar(255),
    foreign key (user_id) references user_info(user_id) on delete cascade,
    foreign key (post_id) references post_info(post_id) on delete cascade
);

create table comment_info(
    comment_id varchar(255),
    comment_text text,
    comment_time datetime,
    post_id varchar(255),
    user_id varchar(255),
    primary key (comment_id),
    foreign key (user_id) references user_info(user_id) on delete cascade,
    foreign key (post_id) references post_info(post_id) on delete cascade
);

create table tag_info(
    tag_id varchar(255),
    tag_name varchar(255),
    primary key (tag_id)
);

create table post_tag(
    post_id varchar(255),
    tag_id varchar(255),
    foreign key (post_id) references post_info(post_id) on delete cascade,
    foreign key (tag_id) references tag_info(tag_id) on delete cascade
);

create table user_follow_tag(
    user_id varchar(255),
    tag_id varchar(255),
    foreign key (user_id) references user_info(user_id) on delete cascade,
    foreign key (tag_id) references tag_info(tag_id) on delete cascade
)
"""

#user_info
sql_insert_user_info="""
insert into user_info (user_id,user_name) values ('{user_id}','{user_name}');
"""

sql_delete_user_info_by_user_id="""
delete from user_info where user_id='{user_id}';
"""

sql_update_user_info_user_name_by_user_id="""
update user_info set user_name='{user_name}' where user_id='{user_id}';
"""

sql_select_user_info_by_user_id="""
select * from user_info where user_id='{user_id}';
"""

#user_security
sql_insert_user_security="""
insert into user_security (user_id,user_email,user_password) values ('{user_id}','{user_email}','{user_password}');
"""

sql_update_user_security_user_email_by_user_id="""
update user_security set user_email='{user_email}' where user_id='{user_id}';
"""

sql_update_user_security_user_password_by_user_id="""
update user_security set user_password='{user_password}' where user_id='{user_id}';
"""

sql_select_user_security_by_user_email_user_password="""
select * from user_security where user_email='{user_email}' and user_password='{user_password}';
"""

sql_select_user_security_by_user_email="""
select * from user_security where user_email='{user_email}';
"""

sql_check_user_security_by_user_id="""
select * from user_security where user_id='{user_id}';
"""

#user_cookie
sql_insert_user_cookie="""
insert into user_cookie (user_id,user_cookie_value,user_cookie_time_stamp) values ('{user_id}','{user_cookie_value}','{user_cookie_time_stamp}');
"""

sql_select_user_cookie_by_user_cookie_value="""
select * from user_cookie where user_cookie_value='{user_cookie_value}';
"""

sql_update_user_cookie_by_user_cookie_value="""
update user_cookie set user_cookie_time_stamp='{user_cookie_time_stamp}' where user_cookie_value='{user_cookie_value}';
"""

sql_delete_user_cookie_by_user_cookie_value="""
delete from user_cookie where user_cookie_value='{user_cookie_value}';
"""

sql_delete_user_cookie_by_user_id="""
delete from user_cookie where user_id='{user_id}';
"""

#user_follow
sql_insert_user_follow="""
insert into user_follow (user_id,follow_id) values ('{user_id}','{follow_id}');
"""

sql_delete_user_follow_by_user_id_follow_id="""
delete from user_follow where user_id='{user_id}' and follow_id='{follow_id}';
"""

sql_select_user_follow_by_user_id="""
select * from user_follow where user_id='{user_id}';
"""

sql_select_user_follow_by_follow_id="""
select * from user_follow where follow_id='{follow_id}';
"""

sql_select_user_follow_with_user_info_by_user_id="""
select * from user_info join (
    select follow_id from user_follow where user_id='{user_id}'
) as user_follow_query on user_follow_query.follow_id=user_info.user_id;
"""

#post_info
sql_insert_post_info="""
insert into post_info (post_id,post_title,post_text,post_time,user_id) values ('{post_id}','{post_title}','{post_text}','{post_time}','{user_id}');
"""

sql_delete_post_info_by_post_id="""
delete from post_info where post_id='{post_id}';
"""

sql_update_post_info_user_name_by_user_id="""
update post_info set user_name='{user_name}' where post_id='{post_id}';
"""

sql_select_post_info_by_post_id="""
select * from post_info where post_id='{post_id}';
"""

sql_select_post_info_by_user_id="""
select * from post_info where post_id='{user_id}';
"""

#post_ingredient
sql_insert_post_ingredient="""
insert into post_ingredient (post_id,ingredient_id,ingredient_text) values ('{post_id}','{ingredient_id}','{ingredient_text}');
"""

sql_delete_post_ingredient_by_post_id="""
delete from post_ingredient where post_id='{post_id}';
"""

sql_delete_post_ingredient_by_ingredient_id="""
delete from post_ingredient where post_id='{ingredient_id}';
"""

sql_select_post_ingredient_by_post_id="""
select * from post_ingredient where post_id='{post_id}';
"""

#user_like_post
sql_insert_user_like_post="""
insert into user_like_post (user_id,post_id) values ('{user_id}','{post_id}');
"""

sql_delete_user_like_post_by_user_id_post_id="""
delete from user_like_post where user_id='{user_id}' and post_id='{post_id}';
"""

#comment_info
sql_insert_comment_info="""
insert into comment_info (comment_id,comment_text,comment_time,post_id,user_id) values ('{comment_id}','{comment_text}','{comment_time}','{post_id}','{user_id}');
"""

sql_delete_comment_info_by_comment_id="""
delete from comment_info where comment_id='{comment_id}';
"""

sql_update_comment_info_by_comment_id="""
update comment_info set comment_text='{comment_text}', comment_time='{comment_time}' where comment_id='{comment_id}';
"""

sql_select_comment_info_by_post_id="""
select * from comment_info where post_id='{post_id}';
"""

#tag_info
sql_insert_tag_info="""
insert into tag_info (tag_id,tag_name) values ('{tag_id}','{tag_name}');
"""

sql_delete_tag_info_by_tag_id="""
delete from tag_info where tag_id='{tag_id}';
"""

#post_tag
sql_insert_post_tag="""
insert into post_tag (post_id,tag_id) values ('{post_id}','{tag_id}');
"""

sql_delete_post_tag_by_post_id_tag_id="""
delete from post_tag where post_id='{post_id}' and tag_id='{tag_id}';
"""

#user_follow_tag
sql_insert_user_follow_tag="""
insert into user_follow_tag (user_id,tag_id) values ('{user_id}','{tag_id}');
"""

sql_delete_user_follow_tag_by_user_id_tag_id="""
delete from user_follow_tag where user_id='{user_id}' and tag_id='{tag_id}';
"""