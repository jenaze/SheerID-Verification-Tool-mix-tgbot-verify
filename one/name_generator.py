"""随机名字生成器 - 使用真实美国人口普查姓名数据"""
import random


# 真实美国名字数据 (基于美国人口普查)
FIRST_NAMES_MALE = [
    "James", "John", "Robert", "Michael", "William", "David", "Joseph", "Charles",
    "Thomas", "Christopher", "Daniel", "Matthew", "Anthony", "Mark", "Donald",
    "Steven", "Andrew", "Paul", "Joshua", "Kenneth", "Kevin", "Brian", "George",
    "Timothy", "Ronald", "Edward", "Jason", "Jeffrey", "Ryan", "Jacob",
    "Ethan", "Noah", "Liam", "Mason", "Lucas", "Benjamin", "Alexander", "Henry",
    "Sebastian", "Jack", "Aiden", "Owen", "Samuel", "Dylan", "Luke", "Gabriel"
]

FIRST_NAMES_FEMALE = [
    "Mary", "Patricia", "Jennifer", "Linda", "Barbara", "Elizabeth", "Susan",
    "Jessica", "Sarah", "Karen", "Lisa", "Nancy", "Betty", "Margaret", "Sandra",
    "Ashley", "Kimberly", "Emily", "Donna", "Michelle", "Dorothy", "Carol",
    "Amanda", "Melissa", "Deborah", "Stephanie", "Rebecca", "Sharon", "Laura",
    "Emma", "Olivia", "Ava", "Isabella", "Sophia", "Mia", "Charlotte", "Amelia",
    "Harper", "Evelyn", "Abigail", "Ella", "Scarlett", "Grace", "Chloe", "Victoria"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
    "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill",
    "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell",
    "Mitchell", "Carter", "Roberts", "Turner", "Phillips", "Evans", "Parker", "Edwards",
    "Collins", "Stewart", "Morris", "Murphy", "Cook", "Rogers", "Morgan", "Peterson"
]


class NameGenerator:
    """英文名字生成器 - 使用真实美国名字"""
    
    @classmethod
    def generate(cls):
        """
        生成随机英文名字
        
        Returns:
            dict: 包含 first_name, last_name, full_name
        """
        # 随机选择性别
        if random.random() < 0.5:
            first_name = random.choice(FIRST_NAMES_MALE)
        else:
            first_name = random.choice(FIRST_NAMES_FEMALE)
        
        last_name = random.choice(LAST_NAMES)
        
        return {
            'first_name': first_name,
            'last_name': last_name,
            'full_name': f"{first_name} {last_name}"
        }


def generate_email(school_domain='MIT.EDU'):
    """
    生成随机学校邮箱
    
    Args:
        school_domain: 学校域名
    
    Returns:
        str: 邮箱地址
    """
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    username = ''.join(random.choice(chars) for _ in range(8))
    return f"{username}@{school_domain}"


def generate_birth_date():
    """
    生成随机生日（2000-2005年）
    
    Returns:
        str: YYYY-MM-DD 格式的日期
    """
    year = 2000 + random.randint(0, 5)
    month = str(random.randint(1, 12)).zfill(2)
    day = str(random.randint(1, 28)).zfill(2)
    return f"{year}-{month}-{day}"

